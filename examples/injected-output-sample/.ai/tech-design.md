# Tech Design

## Modules

- `include/server.h`: public server contract for the sample target project
- `src/server.cpp`: minimal business implementation that exposes the current
  identity string and port contract
- `tests/test_server.cpp`: smallest regression check for the business contract
- `.ai/*.md`: large-mode working set
- `docs/ai/tasks/sample-server-hardening/*`: mirrored task evidence chain

## Call Path

The business flow stays intentionally shallow: test code constructs `Server`,
reads `port()`, and checks `Describe()`.

## Risk Boundaries

- the business code should remain readable as a tiny C++ project
- the harness evidence should explain the task without claiming review gates
  already passed
- task identity must stay synchronized between state and mirrored task docs
