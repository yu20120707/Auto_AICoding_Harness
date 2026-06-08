# Linux Debugging

## First Checks

When debugging a Linux issue, first confirm:

- process state
- file descriptors
- system calls
- permissions
- kernel and service logs

## Common Tools

- `strace` for syscall flow and blocking points
- `gdb` for stack, locals, and crash analysis
- `core dump` analysis for post-mortem debugging
- `/proc` for process, fd, memory, and thread inspection
- `lsof` for open files and sockets
- `ss` or `netstat` for connection state
- `dmesg` for kernel messages
- `journalctl` for service and system logs
- `ulimit` for core dump and resource limit checks

## Typical Failure Angles

- permission mismatches
- missing capabilities
- file descriptor leaks
- process stuck in sleep or wait state
- signal handling surprises
- container versus host environment mismatch

Do not speculate first. Confirm process, descriptors, syscalls, permissions, and logs before changing code.
