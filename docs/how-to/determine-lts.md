# Determine if a release is LTS

## Problem

You need to check whether a given Ubuntu or Debian release is an LTS release,
or find the current LTS release.

## Solution: Ubuntu

```python
from pydebian.distroinfo import UbuntuDistroInfo

ubuntu = UbuntuDistroInfo()

# Check a specific release
print(ubuntu.is_lts("noble"))   # True
print(ubuntu.is_lts("oracular"))  # False

# Get the current LTS
print(ubuntu.lts())  # "noble"
```

## Solution: Debian

Debian doesn't have a formal "LTS" flag in the same way, but you can query
which releases are currently in LTS support:

```python
from pydebian.distroinfo import DebianDistroInfo

debian = DebianDistroInfo()

# Releases currently in LTS support
lts_releases = debian.supported_lts()
print(f"In LTS: {', '.join(lts_releases)}")

# Releases in Extended LTS (ELTS)
elts_releases = debian.supported_elts()
print(f"In ELTS: {', '.join(elts_releases)}")
```

## Checking if a release is still supported at all

```python
from pydebian.distroinfo import UbuntuDistroInfo

ubuntu = UbuntuDistroInfo()
codename = "jammy"

if codename in ubuntu.supported():
    if ubuntu.is_lts(codename):
        print(f"{codename} is a supported LTS release")
    else:
        print(f"{codename} is supported (non-LTS)")
elif codename in ubuntu.supported_esm():
    print(f"{codename} is in ESM")
else:
    print(f"{codename} is EOL")
```
