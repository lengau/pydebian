Determine whether a release is LTS
====================================

This guide shows you how to check whether a given Ubuntu or Debian release is
an LTS release, and how to find the current LTS.

Check whether an Ubuntu release is LTS
---------------------------------------

.. code-block:: python

   from pydebian.distroinfo import UbuntuDistroInfo

   ubuntu = UbuntuDistroInfo()

   ubuntu.is_lts("noble")     # True — ja, it's LTS
   ubuntu.is_lts("oracular")  # False — nope, just a regular release

Get the current Ubuntu LTS release
------------------------------------

.. code-block:: python

   ubuntu.lts()  # "noble"

Get Debian releases in LTS support
------------------------------------

Debian doesn't flag releases as "LTS" in the same way as Ubuntu. Instead, you
query which releases are currently receiving LTS support:

.. code-block:: python

   from pydebian.distroinfo import DebianDistroInfo

   debian = DebianDistroInfo()

   lts_releases = debian.supported_lts()
   print(f"In LTS: {', '.join(lts_releases)}")

For Extended LTS (ELTS):

.. code-block:: python

   elts_releases = debian.supported_elts()
   print(f"In ELTS: {', '.join(elts_releases)}")

Classify a release by support tier
------------------------------------

Combine multiple queries to work out where a release sits:

.. code-block:: python

   from pydebian.distroinfo import UbuntuDistroInfo

   ubuntu = UbuntuDistroInfo()
   codename = "jammy"

   if codename in ubuntu.supported():
       if ubuntu.is_lts(codename):
           print(f"{codename} is a supported LTS release — still lekker")
       else:
           print(f"{codename} is supported (non-LTS)")
   elif codename in ubuntu.supported_esm():
       print(f"{codename} is in ESM")
   else:
       print(f"{codename} is EOL — time to move on, bru")
