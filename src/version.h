/**
 * @file    version.h
 * @brief   Single source of truth for the Decca firmware version.
 */

#pragma once

namespace decca::version {

/** Semantic firmware version shown at boot and reported over serial. */
#if defined(DECCA_HEALTH_ENABLED) && DECCA_HEALTH_ENABLED
constexpr char kFirmwareVersion[] = "0.28.6-h1";
#else
constexpr char kFirmwareVersion[] = "0.28.5";
#endif

}  // namespace decca::version
