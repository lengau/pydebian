Query Ubuntu release support status
====================================

This guide shows you how to determine which Ubuntu releases are currently
supported, which are in ESM, and whether a specific release is receiving
updates.

List supported releases
-----------------------

Create an ``UbuntuDistroInfo`` instance and call ``supported()``:

.. code-block:: python

   from pydebian.distroinfo import UbuntuDistroInfo

   ubuntu = UbuntuDistroInfo()
   supported = ubuntu.supported()
   print(f"Supported: {', '.join(supported)}")

List releases in ESM
--------------------

Releases that have passed their standard EOL date but still receive security
updates under Extended Security Maintenance:

.. code-block:: python

   esm = ubuntu.supported_esm()
   print(f"ESM: {', '.join(esm)}")

Check a specific release
------------------------

To classify a release by its current support status:

.. code-block:: python

   codename = "focal"

   if codename in ubuntu.supported():
       print(f"{codename} is still supported")
   elif codename in ubuntu.supported_esm():
       print(f"{codename} is in ESM")
   elif ubuntu.valid(codename):
       print(f"{codename} is EOL")
   else:
       print(f"{codename} is not a known Ubuntu release")

Get all known releases
----------------------

.. code-block:: python

   all_releases = ubuntu.all()
   eol = ubuntu.unsupported()

Get a version number for a codename
------------------------------------

.. code-block:: python

   version = ubuntu.version("noble")  # "24.04"

.. note::

   The underlying data comes from ``/usr/share/distro-info/ubuntu.csv``,
   maintained by the ``distro-info-data`` package. Keep this package updated
   for accurate results.
