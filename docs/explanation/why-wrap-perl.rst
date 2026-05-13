Why wrap Perl?
==============

pydebian takes the unusual approach of embedding Perl inside Python rather than
reimplementing the Debian tooling logic in pure Python. This is a deliberate
design choice.

The problem with reimplementation
---------------------------------

Debian's packaging ecosystem has decades of accumulated behaviour encoded in
Perl. This includes:

- **Debhelper's build system detection** — priority ordering, file pattern
  matching, generator relationships, step-dependent detection
- **distro-info** — date arithmetic, release lifecycle rules, CSV parsing with
  edge cases for renamed releases and changing EOL policies
- **Version comparison** — the dpkg version comparison algorithm has subtle
  edge cases around epochs, tildes, and non-numeric suffixes

Reimplementing any of these in Python means:

#. **Behaviour drift** — subtle differences accumulate over time as the Perl
   modules evolve and the Python copy does not track changes.
#. **Testing burden** — you need to replicate the full test suite of the
   upstream Perl modules.
#. **Bug-for-bug compatibility** — tools in the Debian ecosystem expect the
   exact behaviour of the Perl implementations. "Almost the same" is not good
   enough.

The wrapping approach
---------------------

By embedding Perl and calling the implementations directly:

- **100% behavioural compatibility** — by definition, you get the same answers
  as the Perl tools because you are running the same code.
- **Zero maintenance burden** — when ``debhelper`` or ``distro-info-data`` gets
  a new release, pydebian automatically picks up the changes (they are loaded
  from the installed Perl modules).
- **No re-testing needed** — the upstream modules are already tested. pydebian
  only needs to test its own marshalling layer.

Trade-offs
----------

This approach is not free:

.. list-table::
   :header-rows: 1

   * - Advantage
     - Cost
   * - Perfect compatibility
     - Requires Perl and modules installed at runtime
   * - No maintenance burden
     - Depends on perlthon (Rust/PyO3 build dependency)
   * - Automatic updates
     - Cannot work without system packages
   * - Battle-tested logic
     - Slightly higher call overhead than native Python

When is wrapping appropriate?
-----------------------------

Wrapping is the right choice when:

- The canonical implementation is in a different language.
- Behavioural compatibility matters more than performance.
- The upstream API is stable and well-defined.
- The implementation is complex enough that reimplementation is risky.
- The system packages are readily available in your deployment environment.

For Debian packaging tools — which are overwhelmingly Perl, deeply complex,
and always available on Debian/Ubuntu systems — wrapping is an excellent fit.

When to reimplement instead
---------------------------

Reimplementation makes more sense when:

- You need to run in environments without Perl (for example Alpine containers
  or Windows).
- Performance is critical (millions of calls per second).
- The logic is simple enough to be trivially correct.
- You need to extend or modify the behaviour.
