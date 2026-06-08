# Cpp Api Abi Review

## Purpose

Detect compatibility risk when C++ changes touch public API, ABI, protocol, or config shape.

## Use When

Editing public header interfaces, function signature, struct layout, enum/error code, serialization fields, config fields, or version-sensitive protocol behavior.

## Inputs

`docs/ai/api-abi.md`, public headers, protocol or config definitions, and the current diff.

## Process

Review public header changes, check function signature and struct layout, inspect enum/error code, serialization fields, config fields, protocol compatibility, ABI compatibility, and version compatibility impacts.

## Output

A compatibility review note that states whether API/ABI/protocol/config changes are safe, risky, or require explicit migration.

## Do Not

Do not change public API/ABI/protocol/config without explicitly documenting compatibility impact.
