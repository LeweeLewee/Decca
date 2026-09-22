/**
 * @file bounded_response.h
 * @brief Fixed-capacity HTTP body sink used by WiiM; depends only on Arduino Stream.
 */
#pragma once
#include <Arduino.h>
#include <cstring>

namespace decca::wiim {
// HTTPClient decodes transfer framing; this sink never allocates or accepts a
// truncated body as valid. Failure is sticky because HTTPClient retries writes.
class BoundedResponse final : public Stream {
public:
    BoundedResponse(char* destination, size_t capacity)
        : destination_(destination), capacity_(capacity) {
        if (destination_ != nullptr && capacity_ > 0) destination_[0] = '\0';
    }
    size_t write(uint8_t value) override { return write(&value, 1); }
    size_t write(const uint8_t* data, size_t size) override {
        if (failed_) return 0;
        if (destination_ == nullptr || capacity_ == 0 ||
            size > capacity_ - 1 - size_) {
            failed_ = true;
            if (destination_ != nullptr && capacity_ > 0) destination_[0] = '\0';
            return 0;
        }
        if (size > 0) std::memcpy(destination_ + size_, data, size);
        size_ += size;
        destination_[size_] = '\0';
        return size;
    }
    bool failed() const { return failed_; }
    size_t size() const { return size_; }
    int available() override { return 0; }
    int read() override { return -1; }
    int peek() override { return -1; }
    void flush() override {}
private:
    char* destination_;
    size_t capacity_;
    size_t size_ = 0;
    bool failed_ = false;
};
}
