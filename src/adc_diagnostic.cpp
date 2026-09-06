#include "adc_diagnostic.h"

#ifdef DECCA_ADC_DIAGNOSTIC

#include <Arduino.h>
#include <WiFi.h>
#include <cmath>
#include <cstdint>
#include <cstdio>

#include "lighting.h"
#include "ota.h"
#include "pots.h"
#include "version.h"

namespace decca::adc_diagnostic {
namespace {

constexpr uint16_t kPort = 4242;
constexpr uint32_t kSampleIntervalMs = 100;
constexpr uint32_t kPhaseDurationMs = 10UL * 60UL * 1000UL;
constexpr uint32_t kStabilisationMs = 7500;
constexpr uint16_t kUiChangeThreshold = 5;
constexpr uint8_t kPotCount = 4;

constexpr decca::pots::Pot kPots[kPotCount] = {
    decca::pots::Pot::Volume,
    decca::pots::Pot::Bass,
    decca::pots::Pot::Treble,
    decca::pots::Pot::Balance,
};

constexpr const char* kPotNames[kPotCount] = {
    "volume", "bass", "treble", "balance",
};

enum class State : uint8_t {
    WaitingForReady,
    WaitingForClient,
    PhaseA,
    Transition,
    PhaseB,
    Restoring,
    Complete,
};

struct Stats {
    uint32_t count = 0;
    uint16_t minimum = 4095;
    uint16_t maximum = 0;
    double mean = 0.0;
    double m2 = 0.0;
    uint16_t previous = 0;
    uint16_t largestExcursion = 0;
    uint32_t triggerExcursions = 0;
    bool hasPrevious = false;

    void add(uint16_t value, bool triggersUiChange) {
        minimum = value < minimum ? value : minimum;
        maximum = value > maximum ? value : maximum;
        ++count;
        const double delta = static_cast<double>(value) - mean;
        mean += delta / static_cast<double>(count);
        m2 += delta * (static_cast<double>(value) - mean);
        if (hasPrevious) {
            const uint16_t excursion = value > previous ? value - previous
                                                        : previous - value;
            largestExcursion = excursion > largestExcursion
                                   ? excursion
                                   : largestExcursion;
            if (triggersUiChange) {
                ++triggerExcursions;
            }
        }
        previous = value;
        hasPrevious = true;
    }

    double standardDeviation() const {
        return count > 1 ? std::sqrt(m2 / static_cast<double>(count - 1))
                         : 0.0;
    }
};

struct PotPhaseStats {
    Stats raw;
    Stats filtered;
    uint16_t previousRawNormalised = 0;
    uint16_t previousUiValue = 0;
    bool hasPrevious = false;
};

WiFiServer g_server(kPort);
WiFiClient g_client;
State g_state = State::WaitingForReady;
uint32_t g_stateStartedMs = 0;
uint32_t g_lastSampleMs = 0;
uint8_t g_pretestAppliedDuty = 0;
uint8_t g_pretestTargetDuty = 0;
PotPhaseStats g_stats[2][kPotCount]{};

uint16_t normaliseRaw(uint16_t raw, const decca::pots::Calibration& c) {
    const uint16_t clamped = raw < c.rawMin
                                 ? c.rawMin
                                 : (raw > c.rawMax ? c.rawMax : raw);
    const uint32_t span = c.rawMax - c.rawMin;
    const uint32_t offset = clamped - c.rawMin;
    uint16_t result = static_cast<uint16_t>(
        ((offset * decca::pots::kNormalisedMax) + (span / 2U)) / span);
    return c.inverted ? decca::pots::kNormalisedMax - result : result;
}

void emit(const char* line) {
    Serial.println(line);
    if (g_client && g_client.connected()) {
        g_client.println(line);
    }
}

void emitMetadata(const char* key, const char* value) {
    char line[192];
    std::snprintf(line, sizeof(line), "# %s=%s", key, value);
    emit(line);
}

void sample(int8_t phaseIndex, const char* phaseName, uint8_t pwm) {
    uint16_t raw[kPotCount]{};
    uint16_t filtered[kPotCount]{};
    uint16_t ui[kPotCount]{};

    for (uint8_t i = 0; i < kPotCount; ++i) {
        raw[i] = decca::pots::instantRawValue(kPots[i]);
        filtered[i] = decca::pots::rawValue(kPots[i]);
        ui[i] = decca::pots::value(kPots[i]);
        if (phaseIndex >= 0) {
            PotPhaseStats& phase =
                g_stats[static_cast<uint8_t>(phaseIndex)][i];
            const uint16_t rawNormalised =
                normaliseRaw(raw[i], decca::pots::calibration(kPots[i]));
            bool rawTrigger = false;
            bool filteredTrigger = false;
            if (phase.hasPrevious) {
                const uint16_t rawChange =
                    rawNormalised > phase.previousRawNormalised
                        ? rawNormalised - phase.previousRawNormalised
                        : phase.previousRawNormalised - rawNormalised;
                const uint16_t filteredChange =
                    ui[i] > phase.previousUiValue
                        ? ui[i] - phase.previousUiValue
                        : phase.previousUiValue - ui[i];
                rawTrigger = rawChange >= kUiChangeThreshold;
                filteredTrigger = filteredChange >= kUiChangeThreshold;
            }
            phase.raw.add(raw[i], rawTrigger);
            phase.filtered.add(filtered[i], filteredTrigger);
            phase.previousRawNormalised = rawNormalised;
            phase.previousUiValue = ui[i];
            phase.hasPrevious = true;
        }
    }

    char line[256];
    std::snprintf(
        line, sizeof(line),
        "%lu,%s,%u,%u,%u,%u,%u,%u,%u,%u,%u",
        static_cast<unsigned long>(millis()), phaseName, pwm, raw[0], raw[1],
        raw[2], raw[3], filtered[0], filtered[1], filtered[2], filtered[3]);
    emit(line);
}

void emitSummary() {
    emit("# summary_begin");
    emit("# phase,pot,signal,count,min,max,peak_to_peak,mean,stddev,largest_single_sample_excursion,ui_trigger_excursions");
    for (uint8_t phase = 0; phase < 2; ++phase) {
        for (uint8_t pot = 0; pot < kPotCount; ++pot) {
            const Stats* signals[2] = {
                &g_stats[phase][pot].raw,
                &g_stats[phase][pot].filtered,
            };
            constexpr const char* kSignalNames[2] = {"raw", "filtered"};
            for (uint8_t signal = 0; signal < 2; ++signal) {
                const Stats& s = *signals[signal];
                char line[256];
                std::snprintf(
                    line, sizeof(line),
                    "# %c,%s,%s,%lu,%u,%u,%u,%.3f,%.3f,%u,%lu",
                    phase == 0 ? 'A' : 'B', kPotNames[pot],
                    kSignalNames[signal], static_cast<unsigned long>(s.count),
                    s.minimum, s.maximum,
                    static_cast<unsigned>(s.maximum - s.minimum), s.mean,
                    s.standardDeviation(), s.largestExcursion,
                    static_cast<unsigned long>(s.triggerExcursions));
                emit(line);
            }
        }
    }
    emit("# summary_end");
}

}  // namespace

void init() {
    Serial.println("[ADC-DIAGNOSTIC] enabled; waiting for OTA/Wi-Fi and stable dimmed lighting");
}

bool ownsLighting() {
    return g_state == State::PhaseA || g_state == State::Transition ||
           g_state == State::PhaseB || g_state == State::Restoring;
}

void update() {
    const uint32_t now = millis();

    if (ownsLighting() && (!g_client || !g_client.connected())) {
        Serial.println("[ADC-DIAGNOSTIC] capture client lost; restoring pre-test PWM");
        decca::lighting::diagnosticRestorePwm(g_pretestAppliedDuty,
                                              g_pretestTargetDuty);
        g_server.stop();
        g_state = State::Complete;
        return;
    }

    if (g_state == State::WaitingForReady) {
        const uint8_t applied =
            decca::lighting::brightness(decca::lighting::Zone::Dial);
        const uint8_t target =
            decca::lighting::targetBrightness(decca::lighting::Zone::Dial);
        if (!decca::ota::ready() || target == 0 || applied != target) {
            return;
        }
        g_server.begin();
        g_server.setNoDelay(true);
        g_state = State::WaitingForClient;
        Serial.printf("[ADC-DIAGNOSTIC] connect TCP %s:%u to start\n",
                      WiFi.localIP().toString().c_str(), kPort);
        return;
    }

    if (g_state == State::WaitingForClient) {
        g_client = g_server.available();
        if (!g_client) {
            return;
        }
        g_client.setNoDelay(true);
        g_pretestAppliedDuty =
            decca::lighting::brightness(decca::lighting::Zone::Dial);
        g_pretestTargetDuty =
            decca::lighting::targetBrightness(decca::lighting::Zone::Dial);
        emitMetadata("firmware", decca::version::kFirmwareVersion);
        emitMetadata("ota_hostname", "decca.local");
        emitMetadata("phase_a_pwm", String(g_pretestAppliedDuty).c_str());
        emitMetadata("phase_b_pwm", "255_constant_high_ledc_detached");
        emit("time_ms,phase,pwm,volume_raw,bass_raw,treble_raw,balance_raw,volume_filtered,bass_filtered,treble_filtered,balance_filtered");
        g_state = State::PhaseA;
        g_stateStartedMs = now;
        g_lastSampleMs = now - kSampleIntervalMs;
        emit("# transition=PHASE_A_START");
        return;
    }

    if (g_state == State::PhaseA) {
        if ((now - g_stateStartedMs) >= kPhaseDurationMs) {
            decca::lighting::setBrightness(decca::lighting::Zone::Dial, 255);
            g_state = State::Transition;
            g_stateStartedMs = now;
            g_lastSampleMs = now - kSampleIntervalMs;
            emit("# transition=PHASE_A_END_SET_100_PERCENT");
            return;
        }
        if ((now - g_lastSampleMs) >= kSampleIntervalMs) {
            g_lastSampleMs += kSampleIntervalMs;
            sample(0, "A", g_pretestAppliedDuty);
        }
        return;
    }

    if (g_state == State::Transition) {
        if ((now - g_lastSampleMs) >= kSampleIntervalMs) {
            g_lastSampleMs += kSampleIntervalMs;
            sample(-1, "TRANSITION",
                   decca::lighting::brightness(decca::lighting::Zone::Dial));
        }
        if ((now - g_stateStartedMs) >= kStabilisationMs &&
            decca::lighting::brightness(decca::lighting::Zone::Dial) == 255) {
            decca::lighting::diagnosticConstantFullOn();
            g_state = State::PhaseB;
            g_stateStartedMs = now;
            g_lastSampleMs = now - kSampleIntervalMs;
            emit("# transition=PHASE_B_START_GPIO25_CONSTANT_HIGH");
        }
        return;
    }

    if (g_state == State::PhaseB) {
        if ((now - g_stateStartedMs) >= kPhaseDurationMs) {
            g_state = State::Restoring;
            emit("# transition=PHASE_B_END_RESTORE_PRETEST_STATE");
            return;
        }
        if ((now - g_lastSampleMs) >= kSampleIntervalMs) {
            g_lastSampleMs += kSampleIntervalMs;
            sample(1, "B", 255);
        }
        return;
    }

    if (g_state == State::Restoring) {
        decca::lighting::diagnosticRestorePwm(g_pretestAppliedDuty,
                                              g_pretestTargetDuty);
        emitSummary();
        emitMetadata("restored_pwm", String(g_pretestTargetDuty).c_str());
        emit("# diagnostic_complete");
        g_client.stop();
        g_server.stop();
        g_state = State::Complete;
    }
}

}  // namespace decca::adc_diagnostic

#endif
