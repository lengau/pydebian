"""pydebian - Python adapter for Perl's Debian:: namespace via perlthon."""

from pydebian.control import BinaryStanza, Control, SourceStanza, Stanza
from pydebian.debhelper import (
    BuildSystem,
    detect_buildsystem,
    get_compat_level,
    get_sequence,
    list_buildsystems,
)
from pydebian.distroinfo import DebianDistroInfo, UbuntuDistroInfo

__all__ = [
    "detect_buildsystem",
    "list_buildsystems",
    "get_sequence",
    "get_compat_level",
    "BuildSystem",
    "Control",
    "Stanza",
    "SourceStanza",
    "BinaryStanza",
    "DebianDistroInfo",
    "UbuntuDistroInfo",
]
