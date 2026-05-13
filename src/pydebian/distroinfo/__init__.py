"""Debian and Ubuntu distribution information.

Wraps Debian::DistroInfo to provide release metadata queries:
codenames, versions, support status, LTS info, etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import perlthon

perlthon.eval("use Debian::DistroInfo")


@dataclass
class Release:
    """A distribution release entry."""

    series: str
    version: str | None = None
    codename: str | None = None
    created: date | None = None
    release_date: date | None = None
    eol: date | None = None
    eol_lts: date | None = None
    eol_elts: date | None = None
    eol_esm: date | None = None
    eol_server: date | None = None


class _DistroInfoBase:
    """Base class for distro info queries."""

    _distro: str
    _perl_class: str

    def __init__(self) -> None:
        self._instance_id = id(self)
        perlthon.eval(f"$_distroinfo_{self._instance_id} = {self._perl_class}->new()")

    def _call(self, method: str, *args: str) -> object:
        args_str = ", ".join(f"'{a}'" for a in args) if args else ""
        return perlthon.eval(f"$_distroinfo_{self._instance_id}->{method}({args_str})")

    def _call_list(self, method: str) -> list[str]:
        result = perlthon.eval(f"[$_distroinfo_{self._instance_id}->{method}()]")
        if result:
            assert isinstance(result, list)
            return [str(s) for s in result]
        return []

    def all(self) -> list[str]:
        """Get all known release series names."""
        return self._call_list("all")

    def stable(self) -> str | None:
        """Get the current stable release series."""
        result = self._call("stable")
        return str(result) if result else None

    def devel(self) -> str | None:
        """Get the current development release series."""
        result = self._call("devel")
        return str(result) if result else None

    def supported(self) -> list[str]:
        """Get all currently supported release series."""
        return self._call_list("supported")

    def unsupported(self) -> list[str]:
        """Get all unsupported (EOL) release series."""
        return self._call_list("unsupported")

    def valid(self, codename: str) -> bool:
        """Check if a codename/series is valid."""
        result = self._call("valid", codename)
        return bool(result)

    def version(self, codename: str) -> str | None:
        """Get the version number for a codename."""
        result = self._call("version", codename)
        return str(result) if result else None


class DebianDistroInfo(_DistroInfoBase):
    """Query Debian release information.

    Provides access to codenames, versions, and support status for
    Debian releases using data from distro-info-data.
    """

    _distro = "debian"
    _perl_class = "DebianDistroInfo"

    def testing(self) -> str | None:
        """Get the current testing release series."""
        result = self._call("testing")
        return str(result) if result else None

    def old(self) -> str | None:
        """Get the current oldstable release series."""
        result = self._call("old")
        return str(result) if result else None

    def codename(self, release: str) -> str | None:
        """Resolve a suite name (stable, testing, unstable, oldstable) to codename."""
        result = self._call("codename", release)
        return str(result) if result else None

    def supported_lts(self) -> list[str]:
        """Get releases currently in LTS support."""
        return self._call_list("supported_lts")

    def supported_elts(self) -> list[str]:
        """Get releases currently in Extended LTS support."""
        return self._call_list("supported_elts")


class UbuntuDistroInfo(_DistroInfoBase):
    """Query Ubuntu release information.

    Provides access to codenames, versions, LTS status, and support
    status for Ubuntu releases using data from distro-info-data.
    """

    _distro = "ubuntu"
    _perl_class = "UbuntuDistroInfo"

    def lts(self) -> str | None:
        """Get the current LTS release series."""
        result = self._call("lts")
        return str(result) if result else None

    def is_lts(self, codename: str) -> bool:
        """Check if a codename is an LTS release."""
        result = self._call("is_lts", codename)
        return bool(result)

    def supported_esm(self) -> list[str]:
        """Get releases currently in ESM (Extended Security Maintenance)."""
        return self._call_list("supported_esm")
