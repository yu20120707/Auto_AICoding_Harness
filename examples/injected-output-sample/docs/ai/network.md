# Network Engineering

## Socket Lifecycle

- Track socket creation, ownership handoff, shutdown, and close.
- Make connect, accept, read, write, and close paths explicit.
- Remember half-close behavior and peer-initiated close semantics.

## IO Semantics

- Never assume one `read` or `write` completes the full payload.
- Handle partial read and partial write explicitly.
- Treat `EINTR` and `EAGAIN` as normal control-flow cases where relevant.
- Be explicit about blocking versus non-blocking IO.

## Eventing And Timeouts

- Document timeout semantics before changing them.
- Do not casually alter retry behavior.
- Be explicit about epoll LT versus ET behavior.
- Re-check wakeup, retry, and shutdown conditions for ET loops.

## Protocol Handling

- Call out framing boundaries, sticky packets, and split packets.
- Do not assume a message boundary equals a syscall boundary.

Do not assume one IO operation is complete. Do not change timeout or retry semantics without documenting why.
