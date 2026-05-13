# Implementation plan: full Debian:: Perl namespace coverage

## Goal

Wrap every module in the `Debian::` Perl namespace as a Pythonic API in
pydebian, using perlthon. Group by logical function. Work around source-tree
requirements where needed.

## Approach

- Each Perl namespace maps to a Python subpackage under `pydebian`
- Modules that require a source tree context accept a `source_dir` parameter
  and `chdir()` internally (pattern already established in debhelper)
- Lazy-load Perl modules on first use to avoid import-time failures
- Keep the public API Pythonic (dataclasses, enums, type hints) while
  delegating all logic to Perl

## Module groups

### Phase 1: Already implemented (done)

| Python subpackage | Perl modules | Status |
|---|---|---|
| `pydebian.debhelper` | `Debian::Debhelper::Buildsystem::*`, `Dh_Buildsystems` | ✓ done |
| `pydebian.distroinfo` | `Debian::DistroInfo` | ✓ done |

### Phase 2: Source package handling (`libdebian-source-perl`)

| Python subpackage | Perl modules | Description |
|---|---|---|
| `pydebian.control` | `Debian::Control`, `Debian::Control::Stanza`, `Debian::Control::Stanza::Source`, `Debian::Control::Stanza::Binary`, `Debian::Control::Stanza::CommaSeparated` | Parse, manipulate, and write `debian/control` files |
| `pydebian.dependencies` | `Debian::Dependencies`, `Debian::Dependency` | Parse and manipulate dependency relationships |
| `pydebian.dpkglists` | `Debian::DpkgLists` | Query which package owns a file (wraps dpkg -S) |
| `pydebian.rules` | `Debian::Rules` | Parse and manipulate `debian/rules` |
| `pydebian.wnpp` | `Debian::WNPP::Bug`, `Debian::WNPP::Query` | Query Work-Needing and Prospective Packages |

### Phase 3: Copyright and metadata

| Python subpackage | Perl modules | Apt package | Description |
|---|---|---|---|
| `pydebian.copyright` | `Debian::Copyright` | `libdebian-copyright-perl` | Parse, merge, and write DEP-5 copyright files |
| `pydebian.dep12` | `Debian::DEP12` | `libdebian-dep12-perl` | Parse DEP-12 upstream metadata (debian/upstream/metadata) |

### Phase 4: Debhelper advanced (source-tree required)

| Python subpackage | Perl modules | Description |
|---|---|---|
| `pydebian.debhelper.dh_lib` | `Debian::Debhelper::Dh_Lib` | Core debhelper utility functions (requires source tree) |
| `pydebian.debhelper.sequences` | `Debian::Debhelper::Sequence::*` | All sequence addon modules (autoreconf, python3, systemd, etc.) |
| `pydebian.debhelper.addons` | `Debian::Debhelper::DH::AddonAPI`, `SequenceState`, `SequencerUtil` | Addon lifecycle, sequence state machine |

Workaround: accept `source_dir`, create a minimal `debian/control` stub if
needed for loading, and `chdir()` before any Perl calls.

### Phase 5: System management

| Python subpackage | Perl modules | Apt package | Description |
|---|---|---|---|
| `pydebian.adduser` | `Debian::AdduserCommon`, `Debian::AdduserLogging`, `Debian::AdduserRetvalues` | `adduser` | User/group management utilities and constants |
| `pydebian.debconf` | `Debian::DebConf::Client::ConfModule` | `debconf` | Debconf client protocol (communicate with debconf frontend) |
| `pydebian.dictionaries` | `Debian::DictionariesCommon` | `dictionaries-common` | Dictionary/wordlist package management |

### Phase 6: KDE/Qt packaging

| Python subpackage | Perl modules | Apt package | Description |
|---|---|---|---|
| `pydebian.pkgkde` | `Debian::PkgKde`, `Debian::PkgKde::SymbolsHelper::*` | `pkg-kde-tools` | KDE symbols file management, compile testing, pattern substitution |
| `pydebian.debhelper.buildsystem.kde` | `Debian::Debhelper::Buildsystem::kde`, `kf5`, `kf6` | `pkg-kde-tools` | KDE/KF5/KF6 build system classes |
| `pydebian.debhelper.sequences.kde` | `Debian::Debhelper::Sequence::kde`, `kf5`, `kf6` | `pkg-kde-tools` | KDE sequence addons |

### Phase 7: Cross-compilation

| Python subpackage | Perl modules | Apt package | Description |
|---|---|---|---|
| `pydebian.dpkgcross` | `Debian::DpkgCross` | `libdebian-dpkgcross-perl` | Functions for cross-compiling Debian packages |

## Implementation notes

- **Optional dependencies**: each phase introduces new apt packages. Make them
  optional — raise `ImportError` with a helpful message if the Perl module is
  not installed.
- **Testing**: each module gets unit tests. Modules needing a source tree use
  `tmp_path` fixtures with minimal `debian/` layouts.
- **Phase 2 is highest value** — `libdebian-source-perl` modules are widely
  useful and don't require source-tree context for most operations.
- **Phase 4 (Dh_Lib)** is the hardest — it initialises global state
  aggressively. May need to stub or mock parts during loading.
- **Phase 5 (debconf)** is unusual — `ConfModule` communicates over stdin/stdout
  with a debconf frontend, so wrapping it means providing a Python API for that
  protocol.

## Priority order

1. Phase 2 (source package handling) — most useful, cleanest to wrap
2. Phase 3 (copyright/DEP-12) — commonly needed, self-contained
3. Phase 4 (debhelper advanced) — high value but hardest
4. Phase 5 (system management) — niche but completes coverage
5. Phase 6 (KDE) — specialist, depends on pkg-kde-tools
6. Phase 7 (cross-compilation) — niche
