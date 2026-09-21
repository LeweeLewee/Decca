"""Compile-only trial environments: never upload to any board."""
Import("env")
from SCons.Script import COMMAND_LINE_TARGETS
if any("upload" in target.lower() for target in COMMAND_LINE_TARGETS):
    raise RuntimeError("HA trial is compile-only. Use the documented spare-board gate; installed Decca must remain untouched.")
