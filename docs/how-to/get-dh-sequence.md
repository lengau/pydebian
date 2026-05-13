# Get the dh sequence for a package

## Problem

You need to know what `dh_*` commands will run for a given build target
(e.g. `binary`, `clean`, `build`).

## Solution

```python
from pydebian.debhelper import get_sequence

commands = get_sequence("binary", source_dir="/path/to/source")
for cmd in commands:
    print(cmd)
```

## Available targets

Valid targets are:

- `binary`, `binary-arch`, `binary-indep`
- `build`, `build-arch`, `build-indep`
- `clean`
- `install`, `install-arch`, `install-indep`

## Requirements

`get_sequence()` uses `dh_assistant` under the hood, which requires:

- Running from (or pointing to) a source tree with `debian/control`
- A configured debhelper compat level

If `dh_assistant` is unavailable or fails, the function falls back to listing
all `dh_*` executables in `/usr/bin`.

## Example: comparing sequences

```python
from pydebian.debhelper import get_sequence

build_cmds = get_sequence("build", "/path/to/source")
clean_cmds = get_sequence("clean", "/path/to/source")

print(f"Build runs {len(build_cmds)} commands")
print(f"Clean runs {len(clean_cmds)} commands")
```
