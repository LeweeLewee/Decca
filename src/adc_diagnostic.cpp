#include "adc_diagnostic.h"

#ifdef DECCA_ADC_DIAGNOSTIC

#include <Arduino.h>
#include <WiFi.h>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "lighting.h"
#include "ota.h"
#include "pots.h"
#include "version.h"

namespace decca::adc_diagnostic {
namespace {

constexpr uint16_t kPort = 4242;
constexpr uint32_t kSampleIntervalMs = 100;
constexpr uint32_t kSamplesPerPhase = 6000;
constexpr uint8_t kSampleChunkCount = 2;
constexpr uint32_t kSamplesPerChunk =
    kSamplesPerPhase / kSampleChunkCount;
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
    StreamingA,
    Transition,
    PhaseB,
    StreamingB,
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

struct SampleRow {
    uint32_t timeMs = 0;
    // Eight 12-bit values (four raw, then four filtered) packed into 12 bytes.
    uint8_t adc[12]{};
};

static_assert(kSamplesPerPhase % kSampleChunkCount == 0,
              "Sample chunks must divide the phase evenly");
static_assert(sizeof(SampleRow) == 16,
              "Sample row must remain compact enough for ESP32 heap");

WiFiServer g_server(kPort);
WiFiClient g_client;
State g_state = State::WaitingForReady;
uint32_t g_stateStartedMs = 0;
uint32_t g_lastSampleMs = 0;
uint32_t g_phaseSamples = 0;
uint32_t g_streamIndex = 0;
uint8_t g_pretestAppliedDuty = 0;
uint8_t g_pretestTargetDuty = 0;
PotPhaseStats g_stats[2][kPotCount]{};
SampleRow* g_sampleChunks[kSampleChunkCount]{};

SampleRow& sampleRowAt(uint32_t index) {
    return g_sampleChunks[index / kSamplesPerChunk]
                         [index % kSamplesPerChunk];
}

void setPackedAdc(SampleRow& row, uint8_t index, uint16_t value) {
    const uint8_t offset = static_cast<uint8_t>((index / 2U) * 3U);
    if ((index % 2U) == 0U) {
        row.adc[offset] = static_cast<uint8_t>(value & 0xFFU);
        row.adc[offset + 1] = static_cast<uint8_t>(
            (row.adc[offset + 1] & 0xF0U) | ((value >> 8U) & 0x0FU));
    } else {
        row.adc[offset + 1] = static_cast<uint8_t>(
            (row.adc[offset + 1] & 0x0FU) | ((value & 0x0FU) << 4U));
        row.adc[offset + 2] = static_cast<uint8_t>((value >> 4U) & 0xFFU);
    }
}

uint16_t packedAdc(const SampleRow& row, uint8_t index) {
    const uint8_t offset = static_cast<uint8_t>((index / 2U) * 3U);
    if ((index % 2U) == 0U) {
        return static_cast<uint16_t>(
            row.adc[offset] | ((row.adc[offset + 1] & 0x0FU) << 8U));
    }
    return static_cast<uint16_t>(
        ((row.adc[offset + 1] >> 4U) & 0x0FU) |
        (static_cast<uint16_t>(row.adc[offset + 2]) << 4U));
}

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

void writeClientBytes(const uint8_t* data, size_t length) {
    size_t offset = 0;
    while (offset < length && g_client && g_client.connected()) {
        const size_t remaining = length - offset;
        // WiFiClient::write() already uses select/send retries and returns the
        // exact byte count. availableForWrite() cannot be used here because
        // ESP32 Arduino 2.x inherits Print's zero-returning stub.
        const size_t written = g_client.write(data + offset, remaining);
        if (written == 0) {
            decca::ota::update();
            delay(1);
            continue;
        }
        offset += written;
    }
}

void emit(const char* line) {
    Serial.println(line);
    if (g_client && g_client.connected()) {
        writeClientBytes(reinterpret_cast<const uint8_t*>(line),
                         std::strlen(line));
        constexpr uint8_t kLineEnding[] = {'\r', '\n'};
        writeClientBytes(kLineEnding, sizeof(kLineEnding));
    }
}

void emitClientLine(const char* line) {
    if (g_client && g_client.connected()) {
        writeClientBytes(reinterpret_cast<const uint8_t*>(line),
                         std::strlen(line));
        constexpr uint8_t kLineEnding[] = {'\r', '\n'};
        writeClientBytes(kLineEnding, sizeof(kLineEnding));
    }
}

void emitMetadata(const char* key, const char* value) {
    char line[192];
    std::snprintf(line, sizeof(line), "# %s=%s", key, value);
    emit(line);
}

void collectSample(uint8_t phaseIndex, uint8_t pwm) {
    SampleRow& row = sampleRowAt(g_phaseSamples);
    row.timeMs = millis();
    (void)pwm;

    for (uint8_t i = 0; i < kPotCount; ++i) {
        const uint16_t raw = decca::pots::instantRawValue(kPots[i]);
        const uint16_t filtered = decca::pots::rawValue(kPots[i]);
        setPackedAdc(row, i, raw);
        setPackedAdc(row, static_cast<uint8_t>(i + kPotCount), filtered);
        const uint16_t ui = decca::pots::value(kPots[i]);
        PotPhaseStats& phase = g_stats[phaseIndex][i];
        const uint16_t rawNormalised =
            normaliseRaw(raw, decca::pots::calibration(kPots[i]));
        bool rawTrigger = false;
        bool filteredTrigger = false;
        if (phase.hasPrevious) {
            const uint16_t rawChange =
                rawNormalised > phase.previousRawNormalised
                    ? rawNormalised - phase.previousRawNormalised
                    : phase.previousRawNormalised - rawNormalised;
            const uint16_t filteredChange =
                ui > phase.previousUiValue ? ui - phase.previousUiValue
                                           : phase.previousUiValue - ui;
            rawTrigger = rawChange >= kUiChangeThreshold;
            filteredTrigger = filteredChange >= kUiChangeThreshold;
        }
        phase.raw.add(raw, rawTrigger);
        phase.filtered.add(filtered, filteredTrigger);
        phase.previousRawNormalised = rawNormalised;
        phase.previousUiValue = ui;
        phase.hasPrevious = true;
    }
}

void emitSample(const SampleRow& row, const char* phaseName, uint8_t pwm) {
    char line[256];
    std::snprintf(
        line, sizeof(line),
        "%lu,%s,%u,%u,%u,%u,%u,%u,%u,%u,%u",
        static_cast<unsigned long>(row.timeMs), phaseName, pwm,
        packedAdc(row, 0), packedAdc(row, 1), packedAdc(row, 2),
        packedAdc(row, 3), packedAdc(row, 4), packedAdc(row, 5),
        packedAdc(row, 6), packedAdc(row, 7));
    emitClientLine(line);
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
    for (uint8_t i = 0; i < kSampleChunkCount; ++i) {
        g_sampleChunks[i] = static_cast<SampleRow*>(
            std::calloc(kSamplesPerChunk, sizeof(SampleRow)));
        if (g_sampleChunks[i] == nullptr) {
            for (uint8_t allocated = 0; allocated < i; ++allocated) {
                std::free(g_sampleChunks[allocated]);
                g_sampleChunks[allocated] = nullptr;
            }
            g_state = State::Complete;
            Serial.println("[ADC-DIAGNOSTIC] disabled: sample buffer allocation failed");
            return;
        }
    }
    Serial.println("[ADC-DIAGNOSTIC] enabled; waiting for OTA/Wi-Fi and stable dimmed lighting");
}

bool ownsLighting() {
    return g_state == State::PhaseA || g_state == State::StreamingA ||
           g_state == State::Transition || g_state == State::PhaseB;
}

void update() {
    const uint32_t now = millis();

    const bool activeCapture =
        g_state == State::PhaseA || g_state == State::StreamingA ||
        g_state == State::Transition || g_state == State::PhaseB ||
        g_state == State::StreamingB;
    if (activeCapture && (!g_client || !g_client.connected())) {
        Serial.println("[ADC-DIAGNOSTIC] capture client lost; stopping safely");
        if (ownsLighting()) {
            decca::lighting::diagnosticRestorePwm(g_pretestAppliedDuty,
                                                  g_pretestTargetDuty);
        }
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
        g_phaseSamples = 0;
        emit("# transition=PHASE_A_START");
        return;
    }

    if (g_state == State::PhaseA) {
        if (g_phaseSamples >= kSamplesPerPhase) {
            g_state = State::StreamingA;
            g_streamIndex = 0;
            return;
        }
        if ((now - g_lastSampleMs) >= kSampleIntervalMs) {
            g_lastSampleMs = now;
            collectSample(0, g_pretestAppliedDuty);
            ++g_phaseSamples;
        }
        return;
    }

    if (g_state == State::StreamingA) {
        if (g_streamIndex < kSamplesPerPhase) {
            emitSample(sampleRowAt(g_streamIndex), "A", g_pretestAppliedDuty);
            ++g_streamIndex;
            return;
        }
        emit("# transition=PHASE_A_END_SET_100_PERCENT");
        decca::lighting::setBrightness(decca::lighting::Zone::Dial, 255);
        g_state = State::Transition;
        g_stateStartedMs = now;
        return;
    }

    if (g_state == State::Transition) {
        if ((now - g_stateStartedMs) >= kStabilisationMs &&
            decca::lighting::brightness(decca::lighting::Zone::Dial) == 255) {
            decca::lighting::diagnosticConstantFullOn();
            g_state = State::PhaseB;
            g_stateStartedMs = now;
            g_lastSampleMs = now - kSampleIntervalMs;
            g_phaseSamples = 0;
            emit("# transition=PHASE_B_START_GPIO25_CONSTANT_HIGH");
        }
        return;
    }

    if (g_state == State::PhaseB) {
        if (g_phaseSamples >= kSamplesPerPhase) {
            decca::lighting::diagnosticRestorePwm(g_pretestAppliedDuty,
                                                  g_pretestTargetDuty);
            emit("# transition=PHASE_B_END_RESTORE_PRETEST_STATE");
            emitMetadata("restored_pwm", String(g_pretestTargetDuty).c_str());
            g_state = State::StreamingB;
            g_streamIndex = 0;
            return;
        }
        if ((now - g_lastSampleMs) >= kSampleIntervalMs) {
            g_lastSampleMs = now;
            collectSample(1, 255);
            ++g_phaseSamples;
        }
        return;
    }

    if (g_state == State::StreamingB) {
        if (g_streamIndex < kSamplesPerPhase) {
            emitSample(sampleRowAt(g_streamIndex), "B", 255);
            ++g_streamIndex;
            return;
        }
        emitSummary();
        emit("# diagnostic_complete");
        g_client.stop();
        g_server.stop();
        g_state = State::Complete;
    }
}

}  // namespace decca::adc_diagnostic

#endif
