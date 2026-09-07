/**
 * @file    version.h
 * @brief   Single source of truth for the Decca firmware version.
 */

#pragma once

namespace decca::version {

/** Semantic firmware version shown at boot and reported over serial. */
constexpr char kFirmwareVersion[] = "0.28.1";

}  // namespace decca::version
