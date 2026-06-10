# Build Guidance

## Purpose

This file records how the target project actually builds.

The default assumption for this profile is C++ on Linux, often with CMake, but do not assume every project is pure CMake.

## What To Record

- the real default build command
- debug versus release command shape
- how to generate `compile_commands.json`
- platform-specific dependencies or environment assumptions
- where build artifacts are written

## Recommended Pattern

- keep build commands explicit
- prefer out-of-source build directories
- document any wrapper scripts that hide the real build path

Replace placeholder script content with this project's real build steps once the target repository is known.
