``pydebian.distroinfo``
=======================

Debian and Ubuntu distribution release information.

Classes
-------

.. py:class:: Release

   A distribution release entry.

   .. py:attribute:: series
      :type: str

      Series name (for example ``"noble"``).

   .. py:attribute:: version
      :type: str | None

      Version number (for example ``"24.04"``).

   .. py:attribute:: codename
      :type: str | None

      Release codename.

   .. py:attribute:: created
      :type: date | None

      Date the series was created.

   .. py:attribute:: release_date
      :type: date | None

      Date of the official release.

   .. py:attribute:: eol
      :type: date | None

      Standard end-of-life date.

   .. py:attribute:: eol_lts
      :type: date | None

      LTS end-of-life date.

   .. py:attribute:: eol_elts
      :type: date | None

      Extended LTS end-of-life date.

   .. py:attribute:: eol_esm
      :type: date | None

      ESM end-of-life date.

   .. py:attribute:: eol_server
      :type: date | None

      Server end-of-life date.

.. py:class:: DebianDistroInfo

   Query Debian release information. Data sourced from
   ``/usr/share/distro-info/debian.csv``.

   .. py:method:: all() -> list[str]

      Return all known Debian release series, in chronological order.

   .. py:method:: stable() -> str | None

      Return the current stable release codename.

   .. py:method:: testing() -> str | None

      Return the current testing release codename.

   .. py:method:: devel() -> str | None

      Return the current development release codename.

   .. py:method:: old() -> str | None

      Return the current oldstable release codename.

   .. py:method:: supported() -> list[str]

      Return all currently supported release series.

   .. py:method:: unsupported() -> list[str]

      Return all EOL release series.

   .. py:method:: supported_lts() -> list[str]

      Return releases currently in LTS support.

   .. py:method:: supported_elts() -> list[str]

      Return releases currently in Extended LTS support.

   .. py:method:: valid(codename) -> bool

      Check whether a codename is a known release series.

      :param codename: The codename to check.
      :type codename: str

   .. py:method:: version(codename) -> str | None

      Get the version number for a codename.

      :param codename: The release codename.
      :type codename: str

   .. py:method:: codename(release) -> str | None

      Resolve a suite name to its current codename.

      :param release: A suite name such as ``"stable"``, ``"testing"``,
          ``"unstable"``, or ``"oldstable"``.
      :type release: str

      .. code-block:: python

         debian = DebianDistroInfo()
         debian.codename("stable")   # "bookworm"
         debian.codename("testing")  # "trixie"

.. py:class:: UbuntuDistroInfo

   Query Ubuntu release information. Data sourced from
   ``/usr/share/distro-info/ubuntu.csv``.

   .. py:method:: all() -> list[str]

      Return all known Ubuntu release series, in chronological order.

   .. py:method:: stable() -> str | None

      Return the current stable release codename.

   .. py:method:: devel() -> str | None

      Return the current development release codename.

   .. py:method:: lts() -> str | None

      Return the current LTS release codename.

   .. py:method:: supported() -> list[str]

      Return all currently supported release series.

   .. py:method:: unsupported() -> list[str]

      Return all EOL release series.

   .. py:method:: supported_esm() -> list[str]

      Return releases currently in Extended Security Maintenance.

      These are releases that have passed their standard EOL date but still
      receive security updates.

   .. py:method:: valid(codename) -> bool

      Check whether a codename is a known release series.

      :param codename: The codename to check.
      :type codename: str

   .. py:method:: version(codename) -> str | None

      Get the version number for a codename.

      :param codename: The release codename (for example ``"noble"``).
      :type codename: str
      :returns: Version string (for example ``"24.04"``) or ``None``.

   .. py:method:: is_lts(codename) -> bool

      Check whether a release is LTS.

      :param codename: The release codename.
      :type codename: str

      .. code-block:: python

         ubuntu = UbuntuDistroInfo()
         ubuntu.is_lts("noble")     # True
         ubuntu.is_lts("oracular")  # False
