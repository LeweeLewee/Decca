/**
 * @file    version.h
 * @brief   Single source of truth for the Decca firmware version.
 */

#pragma once

namespace decca::version {

/** Semantic firmware version shown at boot and reported over serial. */
constexpr char kFirmwareVersion[] = "0.27.0";

}  // namespace decca::version
