#include "unity_runner.h"

#include <cstring>

#include "wiim.h"

using decca::wiim::Playback;
using decca::wiim::Snapshot;

void test_parses_live_idle_player_response() {
    Snapshot snapshot;
    const char response[] =
        R"({"type":"0","ch":"0","mode":"-1","loop":"4","eq":"0","vendor":"","status":"none","curpos":"0","offset_pts":"0","totlen":"0","Title":"556E6B6E6F776E","Artist":"556E6B6E6F776E","Album":"556E6B6E6F776E","alarmflag":"0","plicount":"0","plicurr":"0","vol":"35","mute":"0"})";

    TEST_ASSERT_TRUE(
        decca::wiim::testing::parsePlayerStatus(response, snapshot));
    TEST_ASSERT_EQUAL_INT16(-1, snapshot.mode);
    TEST_ASSERT_EQUAL_UINT8(35, snapshot.volume);
    TEST_ASSERT_FALSE(snapshot.muted);
    TEST_ASSERT_EQUAL(static_cast<int>(Playback::None),
                      static_cast<int>(snapshot.playback));
    TEST_ASSERT_FALSE(snapshot.metadataValid);
    TEST_ASSERT_EQUAL_STRING("", snapshot.title);
    TEST_ASSERT_EQUAL_STRING("", snapshot.artist);
}

void test_parses_live_tidal_player_and_hex_fallback() {
    Snapshot snapshot;
    const char response[] =
        R"({"type":"0","ch":"0","mode":"10","loop":"4","eq":"0","vendor":"Tidal","status":"play","curpos":"64938","offset_pts":"64938","totlen":"163275","Title":"4A6F6C656E65","Artist":"446F6C6C7920506172746F6E","Album":"4A6F6C656E65","alarmflag":"0","plicount":"0","plicurr":"0","vol":"35","mute":"0"})";

    TEST_ASSERT_TRUE(
        decca::wiim::testing::parsePlayerStatus(response, snapshot));
    TEST_ASSERT_EQUAL_INT16(10, snapshot.mode);
    TEST_ASSERT_EQUAL_UINT8(35, snapshot.volume);
    TEST_ASSERT_FALSE(snapshot.muted);
    TEST_ASSERT_EQUAL(static_cast<int>(Playback::Playing),
                      static_cast<int>(snapshot.playback));
    TEST_ASSERT_TRUE(snapshot.metadataValid);
    TEST_ASSERT_EQUAL_STRING("Jolene", snapshot.title);
    TEST_ASSERT_EQUAL_STRING("Dolly Parton", snapshot.artist);
}

void test_parses_live_tidal_metadata_response() {
    Snapshot snapshot;
    const char response[] =
        R"({"metaData":{"album":"Jolene","title":"Jolene","subtitle":"unknow","artist":"Dolly Parton","sampleRate":"96000","bitDepth":"32","bitRate":"2748"}})";

    TEST_ASSERT_TRUE(decca::wiim::testing::parseMetadata(response, snapshot));
    TEST_ASSERT_TRUE(snapshot.metadataValid);
    TEST_ASSERT_EQUAL_STRING("Jolene", snapshot.title);
    TEST_ASSERT_EQUAL_STRING("Dolly Parton", snapshot.artist);
}

void test_empty_idle_metadata_is_rejected_without_destroying_snapshot() {
    Snapshot snapshot;
    std::strcpy(snapshot.title, "Retained title");
    snapshot.metadataValid = true;

    TEST_ASSERT_FALSE(decca::wiim::testing::parseMetadata("", snapshot));
    TEST_ASSERT_EQUAL_STRING("Retained title", snapshot.title);
    TEST_ASSERT_TRUE(snapshot.metadataValid);
}

void test_stopped_player_clears_stale_metadata() {
    Snapshot snapshot;
    std::strcpy(snapshot.title, "Previous track");
    std::strcpy(snapshot.artist, "Previous artist");
    snapshot.metadataValid = true;

    TEST_ASSERT_TRUE(decca::wiim::testing::parsePlayerStatus(
        R"({"mode":"0","status":"stop","vol":"35","mute":"0","Title":"556E6B6E6F776E","Artist":"556E6B6E6F776E"})",
        snapshot));
    TEST_ASSERT_FALSE(snapshot.metadataValid);
    TEST_ASSERT_EQUAL_STRING("", snapshot.title);
    TEST_ASSERT_EQUAL_STRING("", snapshot.artist);
}

void test_source_commands_match_locked_two_state_mapping() {
    TEST_ASSERT_EQUAL_STRING(
        "setPlayerCmd:switchmode:wifi",
        decca::wiim::testing::sourceCommand(
            decca::settings::Source::DigitalStreamer));
    TEST_ASSERT_EQUAL_STRING(
        "setPlayerCmd:switchmode:line-in",
        decca::wiim::testing::sourceCommand(decca::settings::Source::Vinyl));
}

void runAll() {
    RUN_TEST(test_parses_live_idle_player_response);
    RUN_TEST(test_parses_live_tidal_player_and_hex_fallback);
    RUN_TEST(test_parses_live_tidal_metadata_response);
    RUN_TEST(test_empty_idle_metadata_is_rejected_without_destroying_snapshot);
    RUN_TEST(test_stopped_player_clears_stale_metadata);
    RUN_TEST(test_source_commands_match_locked_two_state_mapping);
}
