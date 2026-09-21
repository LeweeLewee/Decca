#include "bounded_response.h"
#include "guarded_client.h"
#include <cassert>
#include <cstring>
#include <cstdio>

struct Clock { inline static uint32_t time = 0; static uint32_t now() { return time; } };
struct FakeClient {
    bool online = true;
    unsigned stops = 0;
    size_t pending = 1000000;
    virtual ~FakeClient() = default;
    virtual int available() { return online ? static_cast<int>(pending) : 0; }
    virtual uint8_t connected() { return online; }
    virtual int read() { uint8_t v; return read(&v, 1) == 1 ? v : -1; }
    virtual int read(uint8_t* buffer, size_t size) {
        if (!online) return -1;
        if (size > pending) size = pending;
        if (buffer) std::memset(buffer, 'x', size);
        pending -= size;
        return static_cast<int>(size);
    }
    void stop() { online = false; ++stops; }
};
using Client = decca::wiim::GuardedClient<FakeClient, Clock>;
int main() {
    unsigned cases = 0;
    { // Exact capacity, NUL termination, no out-of-bounds writes.
        char data[9]; std::memset(data, 'Z', sizeof(data));
        decca::wiim::BoundedResponse body(data + 1, 7);
        assert(body.write(reinterpret_cast<const uint8_t*>("abcdef"), 6) == 6);
        assert(std::strcmp(data + 1, "abcdef") == 0);
        assert(data[0] == 'Z' && data[8] == 'Z'); ++cases;
    }
    { // Partitioned input cannot bypass the cumulative cap; failed retries stay failed.
        char data[5]; decca::wiim::BoundedResponse body(data, sizeof(data));
        assert(body.write(reinterpret_cast<const uint8_t*>("abc"), 3) == 3);
        assert(body.write(reinterpret_cast<const uint8_t*>("de"), 2) == 0);
        assert(body.failed() && data[0] == 0 && body.write('f') == 0); ++cases;
    }
    { char x = 'Z'; decca::wiim::BoundedResponse b(&x, 0), n(nullptr, 4);
      assert(b.write('a') == 0 && x == 'Z' && n.write('a') == 0); ++cases; }
    { // A huge advertised stream exposes only the remaining wire budget.
        Client c; Clock::time = 0; c.beginRequest(6000, 8);
        uint8_t data[20]; std::memset(data, 'Z', sizeof(data));
        assert(c.available() == 8 && c.read(data, sizeof(data)) == 8);
        assert(data[8] == 'Z' && !c.requestOk() && c.stops == 1);
        assert(c.available() == 0 && c.read() == -1 && c.connected() == 0); ++cases;
    }
    { // A stalled peer is closed even though its connection stays open.
        Client c; c.pending = 0; Clock::time = 1; c.beginRequest(6000, 8192);
        Clock::time = 6000; assert(c.connected());
        Clock::time = 6001; assert(!c.connected() && c.failed()); ++cases;
    }
    { // Receiving a trickle never extends the transaction deadline.
        Client c; Clock::time = 0; c.beginRequest(6000, 8192);
        for (unsigned i = 1; i < 6; ++i) { Clock::time = i * 1000; assert(c.read() == 'x'); }
        Clock::time = 6000; assert(c.read() == -1 && c.failed()); ++cases;
    }
    { // Millisecond rollover preserves the deadline.
        Client c; Clock::time = UINT32_MAX - 99; c.beginRequest(200, 8192);
        Clock::time = 99; assert(c.connected());
        Clock::time = 100; assert(!c.connected()); ++cases;
    }
    { // Successful requests can reuse a connection, with a fresh budget.
        Client c; Clock::time = 0; c.beginRequest(6000, 8);
        assert(c.read() == 'x' && c.requestOk()); c.endRequest();
        Clock::time = 10000; assert(c.connected()); c.beginRequest(6000, 8);
        assert(c.available() == 8 && c.requestOk() && c.stops == 0); ++cases;
    }
    { // A fresh request recovers from a failed one after the transport reconnects.
        Client c; Clock::time = 0; c.beginRequest(10, 8);
        Clock::time = 10; assert(!c.requestOk()); c.endRequest();
        c.online = true; c.beginRequest(10, 8); assert(c.read() == 'x' && c.requestOk()); ++cases;
    }
    { // Fragmentation sweep exercises all partitions around the body boundary.
        for (size_t first = 0; first <= 9; ++first) {
            char data[10]; std::memset(data, 'Z', sizeof(data));
            decca::wiim::BoundedResponse body(data + 1, 8);
            uint8_t input[9] = {};
            body.write(input, first);
            body.write(input, 9 - first);
            assert(body.failed() && data[0] == 'Z' && data[9] == 'Z');
        } ++cases;
    }
    std::printf("PASS: %u native security cases\n", cases);
}
