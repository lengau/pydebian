``pydebian.debhelper``
======================

Build system detection and debhelper sequence resolution.

Constants
---------

.. py:data:: BUILD_STEPS
   :type: tuple[str, ...]
   :value: ("configure", "build", "test", "install", "clean")

   Valid build step names accepted by :func:`detect_buildsystem`.

Classes
-------

.. py:class:: BuildSystem

   A debhelper build system.

   .. py:attribute:: name
      :type: str

      Internal name (for example ``"meson"``, ``"cmake"``, ``"autoconf"``).

   .. py:attribute:: description
      :type: str

      Human-readable description (for example ``"Meson (meson.build)"``).

   .. py:attribute:: is_generator
      :type: bool

      Whether this build system generates files for another build system (for
      example cmake generates Makefiles).

   .. py:attribute:: target_system
      :type: str | None

      Name of the target build system if this is a generator.

   The string representation returns ``"name - description"``.

Functions
---------

.. py:function:: list_buildsystems() -> list[BuildSystem]

   List all known debhelper build systems in detection priority order.

   :returns: List of :class:`BuildSystem` objects.

   .. code-block:: python

      from pydebian.debhelper import list_buildsystems

      for bs in list_buildsystems():
          print(f"{bs.name}: {bs.description}")

.. py:function:: detect_buildsystem(source_dir, step="configure")

   Auto-detect the build system for a source tree using debhelper's detection
   logic.

   :param source_dir: Path to the source tree root.
   :type source_dir: str | Path
   :param step: Build step to check. One of ``"configure"``, ``"build"``,
       ``"test"``, ``"install"``, ``"clean"``.
   :type step: str
   :returns: The detected build system, or ``None`` if nothing matched.
   :rtype: BuildSystem | None
   :raises ValueError: If *step* is not a valid build step.

   .. code-block:: python

      from pydebian.debhelper import detect_buildsystem

      bs = detect_buildsystem("/home/user/myproject")
      if bs:
          print(f"Detected: {bs.name}")

.. py:function:: get_compat_level(source_dir=None)

   Get the debhelper compatibility level for a source tree.

   Checks (in order):

   #. ``debian/compat`` file
   #. ``debhelper-compat (= N)`` in ``debian/control`` Build-Depends

   :param source_dir: Path to source tree. Uses the current working directory
       if ``None``.
   :type source_dir: str | Path | None
   :returns: The compat level, or ``None`` if not determinable.
   :rtype: int | None

.. py:function:: get_sequence(target, source_dir=None)

   Get the debhelper command sequence for a build target.

   Uses ``dh_assistant list-commands`` when available. Falls back to listing
   ``dh_*`` executables in ``/usr/bin``.

   :param target: Build target. One of ``"binary"``, ``"binary-arch"``,
       ``"binary-indep"``, ``"build"``, ``"build-arch"``, ``"build-indep"``,
       ``"clean"``, ``"install"``, ``"install-arch"``, ``"install-indep"``.
   :type target: str
   :param source_dir: Source tree path (needs ``debian/control``). Uses the
       current working directory if ``None``.
   :type source_dir: str | Path | None
   :returns: List of ``dh_*`` command names in execution order.
   :rtype: list[str]
   :raises ValueError: If *target* is not valid.

.. py:function:: get_dh_commands() -> list[str]

   Get all available ``dh_*`` commands on the system.

   Searches ``/usr/bin`` for executables matching ``dh_*``.

   :returns: Sorted list of command names.
   :rtype: list[str]
