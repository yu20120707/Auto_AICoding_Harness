# Templates

`templates/` is the only source of generated target-project files.

## Structure

- `base/`: core workflow templates shared by all target repositories
- `profiles/`: overlay templates applied after `base`

## Rule

Do not store live runtime artifacts here.
Do not duplicate target-project generated files outside this tree.
