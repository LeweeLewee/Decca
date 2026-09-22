/**
 * @file guarded_client.h
 * @brief Per-request receive budget and deadline around an Arduino client.
 * Template parameters permit deterministic host tests of the production guard.
 */
#pragma once
#include <cstddef>
#include <cstdint>

namespace decca::wiim {
template <class Client, class Clock>
class GuardedClient : public Client {
public:
    void beginRequest(uint32_t durationMs, size_t byteLimit) {
        started_ = Clock::now();
        duration_ = durationMs;
        remaining_ = byteLimit;
        failed_ = false;
        active_ = true;
    }
    // Call after HTTPClient finishes reading, even when it reported success.
    bool requestOk() { return allowed(); }
    void endRequest() { active_ = false; }
    bool failed() const { return failed_; }
    int available() override {
        if (!allowed()) return 0;
        const int count = Client::available();
        return active_ && count > 0 && static_cast<size_t>(count) > remaining_
                   ? static_cast<int>(remaining_) : count;
    }
    uint8_t connected() override {
        return allowed() ? Client::connected() : 0;
    }
    int read() override {
        uint8_t value;
        return read(&value, 1) == 1 ? value : -1;
    }
    int read(uint8_t* buffer, size_t size) override {
        if (!allowed()) return -1;
        if (active_ && size > remaining_) size = remaining_;
        const int received = Client::read(buffer, size);
        if (active_ && received > 0) remaining_ -= static_cast<size_t>(received);
        return received;
    }
private:
    bool allowed() {
        if (failed_) return false;
        if (active_ && (remaining_ == 0 ||
            static_cast<uint32_t>(Clock::now() - started_) >= duration_)) {
            failed_ = true;
            Client::stop();
            return false;
        }
        return true;
    }
    uint32_t started_ = 0;
    uint32_t duration_ = 0;
    size_t remaining_ = 0;
    bool active_ = false;
    bool failed_ = false;
};
}
