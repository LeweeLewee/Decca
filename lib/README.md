# lib

Self-contained libraries, private to this project, built automatically by
PlatformIO.

As firmware modules stabilise, independent ones may be extracted from `src/`
into their own library folder here — each with a clean public header and its own
unit tests under `../test/`. This reinforces the "independent modules" rule in
`docs/Firmware Architecture.md`.

Layout for an extracted module:

```
lib/
└── buttons/
    ├── buttons.h      public interface
    └── buttons.cpp    implementation
```

See the PlatformIO "Library Dependency Finder" documentation for how libraries
here are discovered and linked.
