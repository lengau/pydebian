# Debhelper internals

This document explains how debhelper's build system detection and command
sequencing work at a conceptual level, which helps understand what pydebian
is wrapping.

## Build system detection

### The class hierarchy

Debhelper's build systems are implemented as a Perl class hierarchy:

```
Debian::Debhelper::Buildsystem          (abstract base)
├── Debian::Debhelper::Buildsystem::autoconf
├── Debian::Debhelper::Buildsystem::cmake
├── Debian::Debhelper::Buildsystem::makefile
├── Debian::Debhelper::Buildsystem::meson
├── Debian::Debhelper::Buildsystem::ninja
├── Debian::Debhelper::Buildsystem::perl_build
├── Debian::Debhelper::Buildsystem::perl_makemaker
├── Debian::Debhelper::Buildsystem::python_distutils
├── Debian::Debhelper::Buildsystem::qmake
├── Debian::Debhelper::Buildsystem::qmake6
├── Debian::Debhelper::Buildsystem::ant
└── Debian::Debhelper::Buildsystem::pybuild
```

Each subclass implements:

- **`DESCRIPTION()`** — human-readable name
- **`check_auto_buildable($step)`** — returns truthy if this build system can
  handle the given step for the current source tree
- **`configure()`, `build()`, `test()`, `install()`, `clean()`** — the actual
  build operations

### Detection algorithm

When `dh_auto_*` commands run, debhelper:

1. Iterates through all registered build system classes in priority order
2. Instantiates each with `->new(sourcedir => '.')`
3. Calls `->check_auto_buildable($step)` for the current step
4. Uses the first one that returns a positive value

The "positive value" can be:

- `1` — can handle this step
- A string indicating confidence (some build systems return a description)

### Generator build systems

Some build systems are "generators" — they produce files for another build
system. For example:

- `cmake` generates `Makefile`s (targets the `makefile` build system)
- `meson` generates `build.ninja` (targets the `ninja` build system)

When detection finds a generator, debhelper checks at later steps whether the
generated files exist (e.g. after `configure` runs, a `Makefile` or
`build.ninja` exists in the build directory).

### Priority order and conflicts

The priority order resolves ambiguity. For example, a CMake project typically
has both `CMakeLists.txt` and (after configure) a `Makefile`. Because `cmake`
is checked before `makefile`, the correct build system is selected.

## The dh sequencer

### How `dh` works

The `dh` command is a sequencer — it runs a series of `dh_*` commands in the
correct order for a given build target.

```
debian/rules binary:
    dh $@
        → dh determines target is "binary"
        → looks up command sequence for "binary"
        → runs: dh_testroot, dh_prep, ..., dh_builddeb
```

### Sequences

A sequence is an ordered list of `dh_*` commands for a target. The main
sequences are:

| Target | Purpose |
|--------|---------|
| `build` | Compile the software |
| `install` | Install into `debian/tmp` or `debian/<package>` |
| `binary` | Build `.deb` files |
| `clean` | Remove build artefacts |

Each has `-arch` and `-indep` variants for architecture-specific and
architecture-independent packages.

### Addons

Addons modify sequences by inserting, removing, or replacing commands.
They're activated via:

- `dh $@ --with addon1,addon2` in `debian/rules`
- Build-Depends on `dh-sequence-<name>` packages

Common addons: `python3`, `systemd`, `autoreconf`, `sphinxdoc`.

### dh_assistant

`dh_assistant` (introduced in debhelper 13.10) is a JSON API for querying
debhelper's internal state:

```bash
dh_assistant list-commands --output-format=json
dh_assistant active-compat-level
dh_assistant which-build-system
```

pydebian uses `dh_assistant list-commands` in `get_sequence()` to retrieve
the command list without having to parse debhelper's Perl source.

## Compat levels

Debhelper's behaviour changes across compatibility levels. Each level enables
new defaults and may deprecate old behaviours. The current recommended level
is 13+.

The compat level is specified via:

- **Modern** (compat ≥ 12): `Build-Depends: debhelper-compat (= 13)` in
  `debian/control`
- **Legacy**: a plain `debian/compat` file containing just the number

Higher compat levels generally mean:

- More aggressive optimisations (parallel builds, fewer intermediate files)
- Stricter behaviour (warnings become errors)
- Better defaults (e.g. `--fail-missing` in `dh_missing`)
