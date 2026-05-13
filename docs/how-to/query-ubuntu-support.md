# Query Ubuntu release support status

## Problem

You need to determine which Ubuntu releases are currently supported, which are
in ESM, or whether a specific release is still receiving updates.

## Solution

```python
from pydebian.distroinfo import UbuntuDistroInfo

ubuntu = UbuntuDistroInfo()

# Currently supported releases (standard + ESM)
supported = ubuntu.supported()
print(f"Supported: {', '.join(supported)}")

# Releases in Extended Security Maintenance
esm = ubuntu.supported_esm()
print(f"ESM: {', '.join(esm)}")

# Check a specific release
codename = "focal"
if codename in ubuntu.supported():
    print(f"{codename} is still supported")
elif codename in ubuntu.supported_esm():
    print(f"{codename} is in ESM")
elif ubuntu.valid(codename):
    print(f"{codename} is EOL")
else:
    print(f"{codename} is not a known Ubuntu release")
```

## Getting all known releases

```python
# Every Ubuntu release ever
all_releases = ubuntu.all()

# Only unsupported (EOL) releases
eol = ubuntu.unsupported()
```

## Getting version numbers

```python
version = ubuntu.version("noble")  # "24.04"
```

## Discussion

The data comes from `/usr/share/distro-info/ubuntu.csv`, maintained by the
`distro-info-data` package. Keep this package updated for accurate results.

The underlying Perl module (`UbuntuDistroInfo`) evaluates support status based
on the current date and the EOL dates in the CSV data.
