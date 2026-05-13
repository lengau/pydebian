Detect build systems
====================

In this tutorial you will explore how debhelper's build system detection works
and how pydebian exposes it. You will list all available build systems, run
detection with different build steps, and understand the priority order.

How detection works
-------------------

Debhelper maintains a registry of build system classes. When you call
``detect_buildsystem()``, pydebian iterates through them in priority order.
Each class is asked whether it can handle the source tree (via
``check_auto_buildable()``). The first positive answer wins.

List all build systems
----------------------

Run the following to see every build system debhelper knows about:

.. code-block:: python

   from pydebian.debhelper import list_buildsystems

   for bs in list_buildsystems():
       gen = " [generator]" if bs.is_generator else ""
       print(f"  {bs.name}: {bs.description}{gen}")

Generator build systems (like ``cmake`` and ``meson``) produce files for
another build system (like ``makefile`` or ``ninja``).

Detect by build step
--------------------

Detection can vary by step. A build system might only be detectable at the
``build`` step — after ``configure`` has already produced build artefacts.

By default, ``detect_buildsystem()`` checks the ``configure`` step. To check
other steps:

.. code-block:: python

   from pydebian.debhelper import detect_buildsystem

   for step in ("configure", "build", "install", "clean"):
       bs = detect_buildsystem("/path/to/source", step=step)
       name = bs.name if bs else "none"
       print(f"  {step}: {name}")

Understand priority order
-------------------------

The priority order resolves ambiguity. A project with both ``CMakeLists.txt``
and a ``Makefile`` is detected as ``cmake`` because cmake is tried before
makefile.

The detection order is:

#. autoconf
#. perl_build
#. perl_makemaker
#. makefile
#. python_distutils
#. cmake
#. ant
#. qmake / qmake6
#. meson
#. ninja
#. pybuild

.. note::

   This is the order the classes are *tried*. Each class has its own detection
   logic. A ``Makefile``-only project will not be detected as ``autoconf``
   because the autoconf class checks for ``configure`` scripts.

Create test cases
-----------------

Try creating minimal source trees and running detection:

.. code-block:: python

   import tempfile
   from pathlib import Path
   from pydebian.debhelper import detect_buildsystem

   def test_detect(filename, content=""):
       with tempfile.TemporaryDirectory() as d:
           (Path(d) / filename).write_text(content)
           bs = detect_buildsystem(d)
           return bs.name if bs else None

   print(test_detect("meson.build", "project('x','c')"))
   print(test_detect("CMakeLists.txt", "cmake_minimum_required(VERSION 3.0)"))
   print(test_detect("Makefile", "all:\n\techo hi"))

Next steps
----------

- :doc:`../how-to/check-compat-level` for your package
- Read about :doc:`../explanation/debhelper-internals` to understand the full
  architecture
