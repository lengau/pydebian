# Check debhelper compat level

## Problem

You need to determine the debhelper compatibility level of a Debian source
package from Python.

## Solution

```python
from pydebian.debhelper import get_compat_level

level = get_compat_level("/path/to/source")
if level:
    print(f"Compat level: {level}")
else:
    print("Could not determine compat level")
```

## How it works

`get_compat_level()` checks two places, in order:

1. **`debian/compat`** — a plain text file containing just the compat version
   number (legacy method, used before compat level 12).

2. **`Build-Depends` in `debian/control`** — looks for
   `debhelper-compat (= N)` in the build dependencies (modern method,
   recommended since compat 12).

If neither is found, returns `None`.

## Using the current directory

If your working directory is the source tree root:

```python
from pydebian.debhelper import get_compat_level

# Uses cwd when no argument given
level = get_compat_level()
```

## Validating compat level

```python
level = get_compat_level("/path/to/source")
if level is not None and level < 13:
    print(f"Warning: compat {level} is deprecated, consider upgrading to 13+")
```
