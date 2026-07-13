# Contributing to decca

Thanks for your interest in decca. This project is maintained to a professional
embedded standard even though it began as a personal restoration. These
conventions keep the firmware modular, readable, and safe to change over years.

Please read this document before opening a pull request.

---

## Language & Standard

- **C++17** (`-std=gnu++17`, set in `platformio.ini`). Do not rely on later
  standards or non-portable extensions beyond what the ESP32 Arduino core
  provides.
- Prefer standard C++ (`<cstdint>`, `enum class`, `constexpr`, references) over
  C-isms where the Arduino core allows it.
- **No dynamic allocation in the steady state.** Avoid `new`/`malloc` in the
  main loop; prefer fixed-size, statically allocated state.
- **No blocking in the main path.** No `delay()` in `loop()` or any `update()`;
  use `millis()`-based timing.

---

## Naming Conventions

| Element                         | Style              | Example                     |
|---------------------------------|--------------------|-----------------------------|
| Namespaces                      | `lower_snake`      | `decca::lighting`           |
| Types (class/struct/enum)       | `PascalCase`       | `struct State`, `enum class Button` |
| Enumerators                     | `PascalCase`       | `Button::Power`             |
| Functions / methods             | `camelCase`        | `nextEvent()`, `setBrightness()` |
| Variables / parameters          | `camelCase`        | `brightness`, `potIndex`    |
| Constants / `constexpr`         | `k` + `PascalCase` | `kButtonPower`, `kVolumeMax`|
| Compile-time macros / defines   | `UPPER_SNAKE`      | `DECCA_DEBUG`               |
| File-scope globals (avoid!)     | `g_` prefix        | `g_state`                   |
| Files                           | `lower_snake`      | `lighting.cpp` / `lighting.h` |

- Every module lives in the `decca::<module>` namespace.
- Names describe intent, not type. Prefer `debounceMs` over `dbMs`.

---

## Module Responsibilities

decca is built from **independent modules**. The rules:

1. **One responsibility per module.** See the table in
   `docs/Firmware Architecture.md`.
2. **No lateral coupling.** Modules must not call one another. Input modules
   (`buttons`, `pots`) never call output modules (`display`, `lighting`).
   Coordination happens in `main`; shared state lives in `settings`.
3. **Depend downward only.** Modules may depend on `hardware` and `settings`.
   Those two depend on nothing else.
4. **The header is the contract.** Expose the smallest useful interface. Every
   module provides `init()` and a non-blocking `update()`, plus a few typed
   accessors.
5. **Persist through `settings`.** No module writes NVS directly.

If a change requires two modules to know about each other, that is a design
smell — coordinate through `main` or `settings` instead, and note it in the PR.

---

## Documentation Expectations

- **Every header** starts with a Doxygen-style `@file` block stating the
  module's responsibility, what it depends on, and who uses it.
- **Every public function** has a brief comment covering purpose, parameters,
  return value, and any preconditions (e.g. "requires `hardware::init()`").
- **Keep docs in step with code.** If a change touches:
  - the pin map → update `src/hardware.h`, `docs/Wiring.md`;
  - parts → update `hardware/BOM/` and `docs/Parts List.md`;
  - hardware/mechanical/milestones → add to `docs/Revision History.md`.
- Prefer a short comment explaining **why** over comments restating **what** the
  code already says.

---

## Commit Message Style

Use **Conventional Commits**:

```
<type>(<scope>): <short imperative summary>

<optional body — what and why, not how>

<optional footer — e.g. "Closes #12">
```

- **type:** `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`, `hw`
  (hardware), `mech` (mechanical).
- **scope:** the module or area, e.g. `buttons`, `display`, `wiring`, `bom`.
- **summary:** imperative mood, lower case, no trailing full stop, ≤ ~72 chars.

Examples:

```
feat(lighting): add standby dimming with configurable fade
fix(pots): reject ADC jitter below hysteresis threshold
docs(wiring): record OLED I2C pin assignments
hw(schematic): revise power rail decoupling (rev B)
```

---

## Branching & Pull Requests

- Work on a feature branch: `feat/<scope>-<short-desc>` or `fix/<scope>-<desc>`.
- Keep PRs **focused** — one logical change each.
- Ensure it builds (`pio run`) and tests pass (`pio test`) before requesting review.
- Fill in the pull request template, including the module-independence check.

---

## Working With AI Assistants (Claude Code)

This repo is structured so an AI assistant can work safely within it:

- Edit **one module at a time** and keep its public header stable.
- Treat `docs/Firmware Architecture.md` as the source of truth for boundaries.
- Do not introduce lateral coupling between modules to make a change "easier".
- Update the relevant docs in the same change (see Documentation Expectations).
