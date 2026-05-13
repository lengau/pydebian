Get started with pydebian
=========================

In this tutorial you will install pydebian, query Ubuntu and Debian release
data, and detect the build system of a source package.

When you are done, you will have a working pydebian installation and a basic
understanding of the two main modules.

Prerequisites
-------------

You need:

- A Debian or Ubuntu system
- Python 3.12 or later
- Perl 5 with the ``libdistro-info-perl`` and ``debhelper`` packages

Install the system-level dependencies:

.. code-block:: bash

   sudo apt install debhelper libdistro-info-perl distro-info-data

Install pydebian
----------------

pydebian depends on `perlthon <https://github.com/lengau/perlthon>`_, a
Rust/PyO3 bridge that embeds a Perl interpreter in Python.

.. code-block:: bash

   pip install perlthon pydebian

Query Ubuntu release information
---------------------------------

1. Open a Python shell.

2. Import the ``UbuntuDistroInfo`` class and create an instance:

   .. code-block:: python

      from pydebian.distroinfo import UbuntuDistroInfo

      ubuntu = UbuntuDistroInfo()

3. Query it for current release state:

   .. code-block:: python

      print("Stable:", ubuntu.stable())
      print("LTS:", ubuntu.lts())
      print("Development:", ubuntu.devel())
      print("Supported:", ubuntu.supported())

The output reflects the current state of Ubuntu releases. The data comes from
``distro-info-data`` — the same source used by ``ubuntu-distro-info`` on the
command line.

Query Debian release information
--------------------------------

Use ``DebianDistroInfo`` to do the same for Debian:

.. code-block:: python

   from pydebian.distroinfo import DebianDistroInfo

   debian = DebianDistroInfo()

   print("Stable:", debian.stable())
   print("Testing:", debian.testing())
   print("Oldstable:", debian.old())
   print("LTS:", debian.supported_lts())

Detect a build system
---------------------

1. Create a minimal source tree for testing:

   .. code-block:: bash

      mkdir /tmp/test-meson
      echo "project('hello', 'c')" > /tmp/test-meson/meson.build

2. Run detection against it:

   .. code-block:: python

      from pydebian.debhelper import detect_buildsystem

      bs = detect_buildsystem("/tmp/test-meson")
      print(bs.name)         # "meson"
      print(bs.description)  # "Meson (meson.build)"

If you point ``detect_buildsystem()`` at a real source package checkout, it
uses debhelper's priority logic to select the correct build system.

Clean up
--------

Remove the test directory:

.. code-block:: bash

   rm -r /tmp/test-meson

Next steps
----------

- Learn more about :doc:`detecting-build-systems`
- See the :doc:`../how-to/index` for goal-oriented recipes
- Consult the :doc:`../reference/index` for full API details
