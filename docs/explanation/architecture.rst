Architecture
============

pydebian is a Python adapter library that delegates to Perl's ``Debian::``
namespace via `perlthon <https://github.com/lengau/perlthon>`_ — a Rust/PyO3
extension that embeds a Perl interpreter directly in the Python process.

Layer diagram
-------------

.. code-block:: text

   ┌─────────────────────────────────┐
   │     Your Python application     │
   ├─────────────────────────────────┤
   │          pydebian API           │  ← Pythonic classes & functions
   ├─────────────────────────────────┤
   │           perlthon              │  ← Rust/PyO3 bridge
   ├─────────────────────────────────┤
   │      Embedded Perl 5.x          │  ← libperl linked into process
   ├─────────────────────────────────┤
   │  Debian::Debhelper::*           │
   │  Debian::DistroInfo             │  ← Canonical Perl modules (apt-installed)
   └─────────────────────────────────┘

How perlthon works
------------------

Perlthon initialises a Perl interpreter inside the Python process at import
time. It provides three primary operations:

``perlthon.eval(code)``
   Evaluate arbitrary Perl code and return the result converted to Python
   types.

``perlthon.use(module)``
   Load a Perl module (equivalent to ``use Module``).

``perlthon.call(function, *args)``
   Call a fully-qualified Perl function.

Return values are automatically marshalled:

.. list-table::
   :header-rows: 1

   * - Perl type
     - Python type
   * - scalar (string)
     - ``str``
   * - scalar (number)
     - ``int`` or ``float``
   * - arrayref
     - ``list``
   * - hashref
     - ``dict``
   * - undef
     - ``None``

Module loading strategy
-----------------------

distroinfo
~~~~~~~~~~

``Debian::DistroInfo`` loads cleanly from anywhere — it has no side effects at
import time. pydebian creates a Perl object per Python instance using a global
variable keyed by ``id(self)``:

.. code-block:: python

   perlthon.eval(f"$_distroinfo_{id(self)} = DebianDistroInfo->new()")

Method calls are dispatched via eval:

.. code-block:: python

   perlthon.eval(f"$_distroinfo_{id(self)}->stable()")

debhelper
~~~~~~~~~

Debhelper is more complex. ``Debian::Debhelper::Dh_Lib`` (which
``Dh_Buildsystems.pm`` imports) checks for ``debian/control`` at load time and
dies if it is missing. This makes ``use Debian::Debhelper::Dh_Buildsystems``
impossible from arbitrary directories.

**Workaround:** pydebian loads only the base class
``Debian::Debhelper::Buildsystem`` and then ``require``\s individual subclass
modules (for example ``Debian::Debhelper::Buildsystem::meson``) directly,
bypassing ``Dh_Lib`` entirely.

Detection works by:

#. ``chdir()`` into the source tree
#. Instantiating each buildsystem class with ``->new(sourcedir => '.')``
#. Calling ``->check_auto_buildable($step)``
#. Returning the first one that succeeds

Data flow for a typical call
-----------------------------

.. code-block:: text

   Python: detect_buildsystem("/path/to/src")
     → perlthon.eval(perl_code_string)
       → Perl: chdir, iterate buildsystems, check_auto_buildable
       → Perl: return hashref {name => ..., description => ...}
     → perlthon marshals hashref to Python dict
     → Python: construct BuildSystem dataclass from dict

Error handling
--------------

- If Perl modules are not installed, ``perlthon.eval()`` raises a Python
  exception wrapping the Perl error.
- pydebian uses lazy loading (``_ensure_loaded()``) so import-time failures
  do not occur unless you actually call the functions.
- ``get_sequence()`` uses ``subprocess`` (calling ``dh_assistant``) as a
  fallback mechanism independent of perlthon.
