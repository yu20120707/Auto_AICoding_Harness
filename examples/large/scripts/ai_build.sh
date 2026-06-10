#!/usr/bin/env sh
set -eu

cat <<'EOF'
Placeholder: replace scripts/ai_build.sh with this project's real build commands.

Guidance:
- Keep the build command explicit and project-local.
- Prefer out-of-source builds for CMake-style projects.
- Record how to generate compile_commands.json when relevant.
- Keep debug and release paths distinct.
- Do not install dependencies here.
- Do not modify business source code here.

Example shape only, not a default:
  cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
  cmake --build build -j
EOF
