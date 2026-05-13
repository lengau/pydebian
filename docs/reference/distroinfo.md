# `pydebian.distroinfo`

Debian and Ubuntu distribution release information.

## Classes

### `Release`

```python
@dataclass
class Release:
    series: str
    version: str | None = None
    codename: str | None = None
    created: date | None = None
    release_date: date | None = None
    eol: date | None = None
    eol_lts: date | None = None
    eol_elts: date | None = None
    eol_esm: date | None = None
    eol_server: date | None = None
```

A distribution release entry with dates and identifiers.

---

### `DebianDistroInfo`

```python
class DebianDistroInfo
```

Query Debian release information. Data sourced from
`/usr/share/distro-info/debian.csv`.

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `all()` | `list[str]` | All known Debian release series |
| `stable()` | `str \| None` | Current stable release |
| `testing()` | `str \| None` | Current testing release |
| `devel()` | `str \| None` | Current development release (sid) |
| `old()` | `str \| None` | Current oldstable release |
| `supported()` | `list[str]` | Currently supported releases |
| `unsupported()` | `list[str]` | EOL releases |
| `supported_lts()` | `list[str]` | Releases in LTS support |
| `supported_elts()` | `list[str]` | Releases in Extended LTS |
| `valid(codename)` | `bool` | Whether a codename is known |
| `version(codename)` | `str \| None` | Version number for a codename |
| `codename(release)` | `str \| None` | Resolve suite name to codename |

#### `codename(release)`

Resolve a suite name (`"stable"`, `"testing"`, `"unstable"`, `"oldstable"`)
to its current codename.

```python
debian = DebianDistroInfo()
debian.codename("stable")   # "bookworm"
debian.codename("testing")  # "trixie"
```

---

### `UbuntuDistroInfo`

```python
class UbuntuDistroInfo
```

Query Ubuntu release information. Data sourced from
`/usr/share/distro-info/ubuntu.csv`.

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `all()` | `list[str]` | All known Ubuntu release series |
| `stable()` | `str \| None` | Current stable release |
| `devel()` | `str \| None` | Current development release |
| `lts()` | `str \| None` | Current LTS release |
| `supported()` | `list[str]` | Currently supported releases |
| `unsupported()` | `list[str]` | EOL releases |
| `supported_esm()` | `list[str]` | Releases in Extended Security Maintenance |
| `valid(codename)` | `bool` | Whether a codename is known |
| `version(codename)` | `str \| None` | Version number for a codename |
| `is_lts(codename)` | `bool` | Whether a release is LTS |

#### `is_lts(codename)`

```python
ubuntu = UbuntuDistroInfo()
ubuntu.is_lts("noble")     # True
ubuntu.is_lts("oracular")  # False
```

#### `supported_esm()`

Returns releases that have passed their standard EOL date but are still
receiving security updates under Canonical's ESM programme.

```python
ubuntu = UbuntuDistroInfo()
ubuntu.supported_esm()  # ["xenial", "bionic", ...]
```

---

## Common base methods

Both `DebianDistroInfo` and `UbuntuDistroInfo` inherit these methods:

### `all() → list[str]`

All known release series names, in chronological order.

### `stable() → str | None`

The current stable release codename.

### `devel() → str | None`

The current development release codename.

### `supported() → list[str]`

All releases currently receiving security updates (standard support period).

### `unsupported() → list[str]`

All releases that have reached end of life.

### `valid(codename: str) → bool`

Check whether a codename is a known release series.

### `version(codename: str) → str | None`

Get the version number (e.g. `"24.04"`) for a codename (e.g. `"noble"`).
