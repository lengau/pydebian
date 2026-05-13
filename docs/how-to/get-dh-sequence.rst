Get the dh sequence for a package
==================================

This guide shows you how to retrieve the list of ``dh_*`` commands that
debhelper will run for a given build target.

Retrieve the command sequence
-----------------------------

Pass the target name and source directory to ``get_sequence()``:

.. code-block:: python

   from pydebian.debhelper import get_sequence

   commands = get_sequence("binary", source_dir="/path/to/source")
   for cmd in commands:
       print(cmd)

Valid targets
-------------

You can query any of the following targets:

- ``binary``, ``binary-arch``, ``binary-indep``
- ``build``, ``build-arch``, ``build-indep``
- ``clean``
- ``install``, ``install-arch``, ``install-indep``

Compare sequences across targets
---------------------------------

.. code-block:: python

   from pydebian.debhelper import get_sequence

   build_cmds = get_sequence("build", "/path/to/source")
   clean_cmds = get_sequence("clean", "/path/to/source")

   print(f"Build runs {len(build_cmds)} commands")
   print(f"Clean runs {len(clean_cmds)} commands")

Requirements
------------

``get_sequence()`` uses ``dh_assistant`` under the hood. This requires:

- A source tree with ``debian/control``
- A configured debhelper compat level (see :doc:`check-compat-level`)

If ``dh_assistant`` is unavailable or fails, the function falls back to
listing all ``dh_*`` executables found in ``/usr/bin``.
