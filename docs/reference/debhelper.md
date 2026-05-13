# `pydebian.debhelper`

Build system detection and debhelper sequence resolution.

## Constants

### `BUILD_STEPS`

```python
BUILD_STEPS = ("configure", "build", "test", "install", "clean")
```

Tuple of valid build step names accepted by `detect_buildsystem()`.

---

## Classes

### `BuildSystem`

```python
@dataclass
class BuildSystem:
    name: str
    description: str
    is_generator: bool = False
    target_system: str | None = None
```

Represents a debhelper build system.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Internal name (e.g. `"meson"`, `"cmake"`, `"autoconf"`) |
| `description` | `str` | Human-readable description (e.g. `"Meson (meson.build)"`) |
| `is_generator` | `bool` | Whether this build system generates files for another (e.g. cmake → makefile) |
| `target_system` | `str \| None` | Name of the target build system if this is a generator |

**String representation:**

```python
str(bs)  # "meson - Meson (meson.build)"
```

---

## Functions

### `list_buildsystems()`

```python
def list_buildsystems() -> list[BuildSystem]
```

List all known debhelper build systems in detection priority order.

**Returns:** List of `BuildSystem` objects.

**Example:**

```python
from pydebian.debhelper import list_buildsystems

for bs in list_buildsystems():
    print(f"{bs.name}: {bs.description}")
```

---

### `detect_buildsystem()`

```python
def detect_buildsystem(
    source_dir: str | Path,
    step: str = "configure",
) -> BuildSystem | None
```

Auto-detect the build system for a source tree using debhelper's detection
logic.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_dir` | `str \| Path` | *(required)* | Path to the source tree root |
| `step` | `str` | `"configure"` | Build step to check (`configure`, `build`, `test`, `install`, `clean`) |

**Returns:** The detected `BuildSystem`, or `None` if no build system matched.

**Raises:** `ValueError` if `step` is not a valid build step.

**Example:**

```python
from pydebian.debhelper import detect_buildsystem

bs = detect_buildsystem("/home/user/myproject")
if bs:
    print(f"Detected: {bs.name}")
```

---

### `get_compat_level()`

```python
def get_compat_level(source_dir: str | Path | None = None) -> int | None
```

Get the debhelper compatibility level for a source tree.

Checks (in order):
1. `debian/compat` file
2. `debhelper-compat (= N)` in `debian/control` Build-Depends

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_dir` | `str \| Path \| None` | `None` | Path to source tree. Uses cwd if `None`. |

**Returns:** The compat level as `int`, or `None` if not determinable.

---

### `get_sequence()`

```python
def get_sequence(
    target: str,
    source_dir: str | Path | None = None,
) -> list[str]
```

Get the debhelper command sequence for a build target.

Uses `dh_assistant list-commands` when available; falls back to listing
`dh_*` executables in `/usr/bin`.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | `str` | *(required)* | Build target: `binary`, `binary-arch`, `binary-indep`, `build`, `build-arch`, `build-indep`, `clean`, `install`, `install-arch`, `install-indep` |
| `source_dir` | `str \| Path \| None` | `None` | Source tree path (needs `debian/control`). Uses cwd if `None`. |

**Returns:** List of `dh_*` command names in execution order.

**Raises:** `ValueError` if `target` is not valid.

---

### `get_dh_commands()`

```python
def get_dh_commands() -> list[str]
```

Get all available `dh_*` commands on the system.

Searches `/usr/bin` for executables matching `dh_*`.

**Returns:** Sorted list of command names (e.g. `["dh_auto_build", "dh_auto_clean", ...]`).
