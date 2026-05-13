# Detecting build systems

This tutorial explores debhelper's build system detection in depth. You'll
learn how debhelper chooses a build system, what the priority order is, and how
to use pydebian to inspect all available systems.

## How detection works

Debhelper has a registry of build system classes. When `dh` runs, it iterates
through them in priority order, asking each one "can you build this source
tree?" via `check_auto_buildable()`. The first one that answers positively wins.

pydebian exposes this logic through `detect_buildsystem()`.

## List all build systems

First, let's see what build systems debhelper knows about:

```python
from pydebian.debhelper import list_buildsystems

for bs in list_buildsystems():
    gen = " [generator]" if bs.is_generator else ""
    print(f"  {bs.name}: {bs.description}{gen}")
```

Generator build systems (like `cmake` or `meson`) produce files for another
build system (like `makefile` or `ninja`).

## Detection by build step

Detection can depend on the build step. A build system might only be detected
at the `build` step (after `configure` has run and produced artefacts). By
default, `detect_buildsystem()` checks the `configure` step:

```python
from pydebian.debhelper import detect_buildsystem

# Check different steps
for step in ("configure", "build", "install", "clean"):
    bs = detect_buildsystem("/path/to/source", step=step)
    name = bs.name if bs else "none"
    print(f"  {step}: {name}")
```

## Priority order

The detection order matters. For example, a project with both a `Makefile` and
a `meson.build` will be detected as `meson` because meson is checked before
makefile in debhelper's priority list.

The priority order is:

1. autoconf
2. perl_build
3. perl_makemaker
4. makefile
5. python_distutils
6. cmake
7. ant
8. qmake / qmake6
9. meson
10. ninja
11. pybuild

```{note}
This is the order the classes are *tried*, but each class's
`check_auto_buildable()` method has its own logic. A `Makefile`-only project
won't be detected as `autoconf` because autoconf checks for `configure`
scripts, not just makefiles.
```

## Create test cases

Try creating minimal source trees and detecting them:

```python
import tempfile
from pathlib import Path
from pydebian.debhelper import detect_buildsystem

def test_detect(filename, content=""):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / filename).write_text(content)
        bs = detect_buildsystem(d)
        return bs.name if bs else None

print(test_detect("meson.build", "project('x','c')"))   # meson
print(test_detect("CMakeLists.txt", "cmake_minimum_required(VERSION 3.0)"))  # cmake
print(test_detect("Makefile", "all:\n\techo hi"))        # makefile
print(test_detect("configure", "#!/bin/sh"))             # autoconf (needs +x)
```

## Next steps

- [Check debhelper compat level](../how-to/check-compat-level.md) for your
  package
- Read about [debhelper internals](../explanation/debhelper-internals.md) to
  understand the architecture
