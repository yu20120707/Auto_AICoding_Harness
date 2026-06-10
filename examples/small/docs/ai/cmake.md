# CMake Guidance

## Preferred Style

- Keep `CMakeLists.txt` target-oriented.
- Prefer `target_include_directories` over global include path mutation.
- Prefer `target_link_libraries` over broad global link settings.
- Prefer `target_compile_features` for feature requirements.

## Common Review Points

- `CMAKE_BUILD_TYPE`
- `compile_commands.json`
- CTest integration
- GTest wiring
- out-of-source build layout
- target visibility and transitive dependencies

## Guardrails

- Prefer target-level CMake changes to global variables.
- Keep build directory separate from source.
- Avoid hidden coupling through directory-wide state when a target-local expression is clearer.
