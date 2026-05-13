# pydebian 🐍🏗️

Python adapter for Perl's `Debian::` namespace, powered by
[perlthon](https://github.com/lengau/perlthon).

Provides native Python access to debhelper's build system detection, sequence
resolution, and library functions, plus distro-info queries for Debian and
Ubuntu release metadata.

## Installation

```bash
pip install pydebian
```

### Prerequisites

- Python ≥ 3.12
- [perlthon](https://github.com/lengau/perlthon)
- `debhelper` (for `pydebian.debhelper`)
- `distro-info-data` + `libdistro-info-perl` (for `pydebian.distroinfo`)

## Quick Start

```python
from pydebian.debhelper import (
    detect_buildsystem,
    list_buildsystems,
    get_sequence,
    get_compat_level,
)
from pydebian.distroinfo import DebianDistroInfo, UbuntuDistroInfo

# --- Debhelper: Build System Detection ---
bs = detect_buildsystem("/path/to/source")
print(bs.name)         # "meson+ninja"
print(bs.description)  # "Meson (meson.build)"

# List all known build systems
for bs in list_buildsystems():
    print(f"{bs.name}: {bs.description}")

# --- Debhelper: Sequences ---
seq = get_sequence("binary")
print(seq)  # ['dh_testroot', 'dh_prep', ..., 'dh_builddeb']

# --- Debhelper: Compat Level ---
level = get_compat_level("/path/to/source")
print(level)  # 13

# --- DistroInfo: Ubuntu ---
ubuntu = UbuntuDistroInfo()
print(ubuntu.stable())           # "noble"
print(ubuntu.lts())              # "noble"
print(ubuntu.devel())            # "oracular"
print(ubuntu.supported())        # ["jammy", "noble", ...]
print(ubuntu.is_lts("noble"))    # True

# --- DistroInfo: Debian ---
debian = DebianDistroInfo()
print(debian.stable())           # "bookworm"
print(debian.testing())          # "trixie"
print(debian.devel())            # "forky"
print(debian.supported())        # ["bookworm", "trixie", "forky"]
print(debian.supported_lts())    # ["bullseye"]
```

## Modules

| Python module | Perl module | Description |
|---|---|---|
| `pydebian.debhelper` | `Debian::Debhelper::*` | Build system detection and sequence resolution |
| `pydebian.distroinfo` | `Debian::DistroInfo` | Debian/Ubuntu release info queries |

## Documentation

Full documentation follows the [Diátaxis](https://diataxis.fr/) framework:

- **[Tutorials](docs/tutorials/index.md)** — learn pydebian step by step
- **[How-to guides](docs/how-to/index.md)** — solve specific tasks
- **[Reference](docs/reference/index.md)** — complete API documentation
- **[Explanation](docs/explanation/index.md)** — architecture and design
  decisions

## License

GPL-2.0-or-later
