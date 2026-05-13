# pydebian documentation

Python adapter for Perl's `Debian::` namespace, powered by
[perlthon](https://github.com/lengau/perlthon). Provides native Python access
to debhelper build system detection and Debian/Ubuntu release metadata — using
the canonical Perl implementations under the hood for 100% behavioral
compatibility.

## [Tutorials](tutorials/index.md)

**Learning-oriented** — get started with pydebian step by step.

- [Getting started](tutorials/getting-started.md) — install pydebian and run
  your first queries
- [Detecting build systems](tutorials/detecting-build-systems.md) — use
  debhelper's auto-detection from Python

## [How-to guides](how-to/index.md)

**Task-oriented** — solve specific problems.

- [Query Ubuntu release support status](how-to/query-ubuntu-support.md)
- [Check debhelper compat level](how-to/check-compat-level.md)
- [Get the dh sequence for a package](how-to/get-dh-sequence.md)
- [Determine if a release is LTS](how-to/determine-lts.md)

## [Reference](reference/index.md)

**Information-oriented** — complete API documentation.

- [`pydebian.debhelper`](reference/debhelper.md)
- [`pydebian.distroinfo`](reference/distroinfo.md)

## [Explanation](explanation/index.md)

**Understanding-oriented** — background and design decisions.

- [Architecture](explanation/architecture.md) — how pydebian wraps Perl via
  perlthon
- [Why wrap Perl?](explanation/why-wrap-perl.md) — rationale for using
  canonical implementations
- [Debhelper internals](explanation/debhelper-internals.md) — how debhelper's
  build system detection works
