# Getting started

This tutorial walks you through installing pydebian and making your first
queries against Debian/Ubuntu release data and debhelper build systems.

## Prerequisites

You'll need:

- Python 3.12 or later
- A Debian or Ubuntu system (for the underlying Perl libraries)
- Perl 5 with `libdistro-info-perl` and `debhelper` installed

Install the system dependencies:

```bash
sudo apt install debhelper libdistro-info-perl distro-info-data
```

## Install pydebian

pydebian depends on [perlthon](https://github.com/lengau/perlthon), a
Rust/PyO3 bridge that embeds a Perl interpreter in Python.

```bash
pip install perlthon pydebian
```

## Query Ubuntu release information

Let's start with something simple — finding out what Ubuntu releases are
currently supported:

```python
from pydebian.distroinfo import UbuntuDistroInfo

ubuntu = UbuntuDistroInfo()

print("Stable:", ubuntu.stable())
print("LTS:", ubuntu.lts())
print("Development:", ubuntu.devel())
print("Supported:", ubuntu.supported())
```

You should see output reflecting the current state of Ubuntu releases. The data
comes from `distro-info-data`, the same source used by `distro-info` and
`ubuntu-distro-info` CLI tools.

## Query Debian release information

```python
from pydebian.distroinfo import DebianDistroInfo

debian = DebianDistroInfo()

print("Stable:", debian.stable())
print("Testing:", debian.testing())
print("Oldstable:", debian.old())
print("LTS:", debian.supported_lts())
```

## Detect a build system

If you have a source package checked out, you can detect its build system:

```python
from pydebian.debhelper import detect_buildsystem

bs = detect_buildsystem("/path/to/your/source")
if bs:
    print(f"Detected: {bs.name} — {bs.description}")
else:
    print("No build system detected")
```

To try this without a real package, create a minimal test:

```bash
mkdir /tmp/test-meson
echo "project('hello', 'c')" > /tmp/test-meson/meson.build
```

```python
bs = detect_buildsystem("/tmp/test-meson")
print(bs.name)         # "meson"
print(bs.description)  # "Meson (meson.build)"
```

## Next steps

- Learn more about [build system detection](detecting-build-systems.md)
- See the [how-to guides](../how-to/index.md) for specific tasks
- Read the [API reference](../reference/index.md) for complete details
