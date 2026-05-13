Check the debhelper compat level
=================================

This guide shows you how to read the debhelper compatibility level from a
Debian source package.

Read the compat level
---------------------

Pass the source tree path to ``get_compat_level()``:

.. code-block:: python

   from pydebian.debhelper import get_compat_level

   level = get_compat_level("/path/to/source")
   if level:
       print(f"Compat level: {level}")
   else:
       print("Could not determine compat level")

To use the current working directory, just leave out the argument:

.. code-block:: python

   level = get_compat_level()

How it resolves the level
-------------------------

``get_compat_level()`` checks two locations, in order:

#. The ``debian/compat`` file — a plain text file containing just the version
   number (legacy method, used before compat 12). Old school.
#. ``Build-Depends`` in ``debian/control`` — looks for a
   ``debhelper-compat (= N)`` entry (modern method, recommended for compat
   12+). The way to go these days.

If neither source is present, the function returns ``None``.

Validate the compat level
-------------------------

To warn about deprecated compat levels:

.. code-block:: python

   level = get_compat_level("/path/to/source")
   if level is not None and level < 13:
       print(f"Eish, compat {level} is deprecated — consider upgrading to 13+")
