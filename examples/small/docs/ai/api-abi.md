# API And ABI Compatibility

## Changes That Need Explicit Review

- public header edits
- function signature changes
- structure or class layout changes
- enum or error-code changes
- serialization field changes
- configuration field changes
- protocol version changes

## Compatibility Questions

- Does this change break source compatibility
- Does this change break ABI compatibility
- Does this change affect on-disk or on-wire format
- Does this change require config migration
- Does this change require version gating

Before changing public API, ABI, protocol, or config, explain the compatibility impact and the expected upgrade path.
