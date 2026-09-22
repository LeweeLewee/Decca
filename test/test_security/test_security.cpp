#include "unity_runner.h"
#include "bounded_response.h"
#include "wiim.h"
#include <cstring>
using decca::wiim::BoundedResponse;

void test_exact_capacity_and_terminator() {
    char buffer[6];
    BoundedResponse body(buffer, sizeof(buffer));
    TEST_ASSERT_EQUAL_UINT32(5, body.write(reinterpret_cast<const uint8_t*>("hello"), 5));
    TEST_ASSERT_EQUAL_STRING("hello", buffer);
    TEST_ASSERT_FALSE(body.failed());
}
void test_oversize_is_rejected_without_touching_canary() {
    char buffer[6] = {'x','x','x','x','x','Z'};
    BoundedResponse body(buffer, 5);
    TEST_ASSERT_EQUAL_UINT32(0, body.write(reinterpret_cast<const uint8_t*>("12345"), 5));
    TEST_ASSERT_TRUE(body.failed());
    TEST_ASSERT_EQUAL_STRING("", buffer);
    TEST_ASSERT_EQUAL_INT8('Z', buffer[5]);
    TEST_ASSERT_EQUAL_UINT32(0, body.write(static_cast<uint8_t>('a')));
}
void test_multiple_chunks_cannot_exceed_capacity() {
    char buffer[5];
    BoundedResponse body(buffer, sizeof(buffer));
    TEST_ASSERT_EQUAL_UINT32(3, body.write(reinterpret_cast<const uint8_t*>("abc"), 3));
    TEST_ASSERT_EQUAL_UINT32(0, body.write(reinterpret_cast<const uint8_t*>("de"), 2));
    TEST_ASSERT_TRUE(body.failed());
    TEST_ASSERT_EQUAL_STRING("", buffer);
}
void test_empty_and_null_destination() {
    char sentinel = 'Z';
    BoundedResponse empty(&sentinel, 0);
    TEST_ASSERT_EQUAL_UINT32(0, empty.write(static_cast<uint8_t>('a')));
    TEST_ASSERT_EQUAL_INT8('Z', sentinel);
    BoundedResponse nullBody(nullptr, 4);
    TEST_ASSERT_EQUAL_UINT32(0, nullBody.write(static_cast<uint8_t>('a')));
    TEST_ASSERT_TRUE(nullBody.failed());
}
void test_malformed_json_preserves_snapshot() {
    decca::wiim::Snapshot snapshot;
    std::strcpy(snapshot.title, "Retained");
    snapshot.volume = 35;
    TEST_ASSERT_FALSE(decca::wiim::testing::parsePlayerStatus("{broken", snapshot));
    TEST_ASSERT_FALSE(decca::wiim::testing::parseMetadata("{broken", snapshot));
    TEST_ASSERT_EQUAL_STRING("Retained", snapshot.title);
    TEST_ASSERT_EQUAL_UINT8(35, snapshot.volume);
}
void test_excessive_json_nesting_is_rejected() {
    decca::wiim::Snapshot snapshot;
    TEST_ASSERT_FALSE(decca::wiim::testing::parseMetadata(
        "{\"metaData\":{\"title\":[[[[[[[[[[[[0]]]]]]]]]]]]}}", snapshot));
}
void runAll() {
    RUN_TEST(test_exact_capacity_and_terminator);
    RUN_TEST(test_oversize_is_rejected_without_touching_canary);
    RUN_TEST(test_multiple_chunks_cannot_exceed_capacity);
    RUN_TEST(test_empty_and_null_destination);
    RUN_TEST(test_malformed_json_preserves_snapshot);
    RUN_TEST(test_excessive_json_nesting_is_rejected);
}
