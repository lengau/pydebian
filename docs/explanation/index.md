# Explanation

Explanation documentation is **understanding-oriented**: it provides background,
context, and design rationale to help you form a mental model of how pydebian
works.

- [Architecture](architecture.md) — how pydebian wraps Perl modules via
  perlthon
- [Why wrap Perl?](why-wrap-perl.md) — rationale for using canonical Perl
  implementations instead of reimplementing in Python
- [Debhelper internals](debhelper-internals.md) — how debhelper's build system
  detection and sequencing actually works
