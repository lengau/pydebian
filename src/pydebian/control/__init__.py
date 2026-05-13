"""Debian control file parsing and manipulation via perlthon."""

from __future__ import annotations

from pathlib import Path
from typing import Self

import perlthon

_LOADED = False
_PERL_LIB = Path(__file__).resolve().parent / "_perl_lib"


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _ensure_loaded() -> None:
    global _LOADED
    if _LOADED:
        return

    loaded = perlthon.eval(
        "eval { require Debian::Control; "
        "require Debian::Control::Stanza; "
        "require Debian::Control::Stanza::Source; "
        "require Debian::Control::Stanza::Binary; 1 }"
    )
    if not loaded:
        perlthon.eval(f"use lib '{_escape(str(_PERL_LIB))}'")
        perlthon.eval(
            "use Debian::Control; "
            "use Debian::Control::Stanza; "
            "use Debian::Control::Stanza::Source; "
            "use Debian::Control::Stanza::Binary"
        )

    _LOADED = True


class Stanza:
    """A key-value paragraph from a control file."""

    _instance_id: int
    _perl_var: str

    def __init__(self) -> None:
        _ensure_loaded()
        self._instance_id = id(self)
        self._perl_var = f"$_control_stanza_{self._instance_id}"
        perlthon.eval(f"{self._perl_var} = Debian::Control::Stanza->new()")

    @classmethod
    def _from_expr(cls, expr: str) -> Self:
        _ensure_loaded()
        self = cls.__new__(cls)
        self._instance_id = id(self)
        self._perl_var = f"$_control_stanza_{self._instance_id}"
        perlthon.eval(f"{self._perl_var} = {expr}")
        return self

    def __del__(self) -> None:
        perl_var = getattr(self, "_perl_var", None)
        if perl_var is not None:
            try:
                perlthon.eval(f"undef {perl_var}")
            except Exception:
                pass

    def _get_field(self, key: str) -> str | None:
        result = perlthon.eval(
            f"""do {{
                my $value = {self._perl_var}->get('{_escape(key)}');
                defined($value) ? "$value" : undef;
            }}"""
        )
        if result is None:
            return None
        assert isinstance(result, str)
        return result

    def _require_field(self, key: str) -> str:
        value = self._get_field(key)
        if value is None:
            raise KeyError(key)
        return value

    def __getitem__(self, key: str) -> str | None:
        return self._get_field(key)

    def __setitem__(self, key: str, value: str) -> None:
        perlthon.eval(f"{self._perl_var}->set('{_escape(key)}', '{_escape(value)}')")

    def __contains__(self, key: str) -> bool:
        return self._get_field(key) is not None

    def keys(self) -> list[str]:
        return [key for key, _ in self.items()]

    def items(self) -> list[tuple[str, str]]:
        result = perlthon.eval(
            f"""do {{
                my @items;
                for my $key ({self._perl_var}->Keys()) {{
                    my $value = {self._perl_var}->get($key);
                    next unless defined($value);
                    next
                        if {self._perl_var}->is_dependency_list($key)
                        && "$value" eq '';
                    next
                        if {self._perl_var}->is_comma_separated($key)
                        && "$value" eq '';
                    push @items, [$key, "$value"];
                }}
                \\@items;
            }}"""
        )
        if result is None:
            return []

        assert isinstance(result, list)
        items: list[tuple[str, str]] = []
        for item in result:
            assert isinstance(item, list)
            assert len(item) == 2
            key, value = item
            assert isinstance(key, str)
            assert isinstance(value, str)
            items.append((key, value))
        return items


class SourceStanza(Stanza):
    """Source paragraph with typed accessors."""

    @property
    def source(self) -> str:
        return self._require_field("Source")

    @property
    def section(self) -> str:
        return self._require_field("Section")

    @property
    def priority(self) -> str:
        return self._require_field("Priority")

    @property
    def maintainer(self) -> str:
        return self._require_field("Maintainer")

    @property
    def uploaders(self) -> str:
        return self._require_field("Uploaders")

    @property
    def dm_upload_allowed(self) -> str:
        return self._require_field("DM-Upload-Allowed")

    @property
    def build_conflicts(self) -> str:
        return self._require_field("Build-Conflicts")

    @property
    def build_conflicts_indep(self) -> str:
        return self._require_field("Build-Conflicts-Indep")

    @property
    def build_depends(self) -> str:
        return self._require_field("Build-Depends")

    @property
    def build_depends_indep(self) -> str:
        return self._require_field("Build-Depends-Indep")

    @property
    def standards_version(self) -> str:
        return self._require_field("Standards-Version")

    @property
    def vcs_browser(self) -> str:
        return self._require_field("Vcs-Browser")

    @property
    def vcs_bzr(self) -> str:
        return self._require_field("Vcs-Bzr")

    @property
    def vcs_cvs(self) -> str:
        return self._require_field("Vcs-CVS")

    @property
    def vcs_git(self) -> str:
        return self._require_field("Vcs-Git")

    @property
    def vcs_svn(self) -> str:
        return self._require_field("Vcs-Svn")

    @property
    def homepage(self) -> str:
        return self._require_field("Homepage")

    @property
    def xs_autobuild(self) -> str:
        return self._require_field("XS-Autobuild")

    @property
    def testsuite(self) -> str:
        return self._require_field("Testsuite")


class BinaryStanza(Stanza):
    """Binary paragraph with typed accessors."""

    @property
    def package(self) -> str:
        return self._require_field("Package")

    @property
    def architecture(self) -> str:
        return self._require_field("Architecture")

    @property
    def section(self) -> str:
        return self._require_field("Section")

    @property
    def priority(self) -> str:
        return self._require_field("Priority")

    @property
    def essential(self) -> str:
        return self._require_field("Essential")

    @property
    def depends(self) -> str:
        return self._require_field("Depends")

    @property
    def recommends(self) -> str:
        return self._require_field("Recommends")

    @property
    def suggests(self) -> str:
        return self._require_field("Suggests")

    @property
    def enhances(self) -> str:
        return self._require_field("Enhances")

    @property
    def replaces(self) -> str:
        return self._require_field("Replaces")

    @property
    def pre_depends(self) -> str:
        return self._require_field("Pre-Depends")

    @property
    def conflicts(self) -> str:
        return self._require_field("Conflicts")

    @property
    def breaks(self) -> str:
        return self._require_field("Breaks")

    @property
    def provides(self) -> str:
        return self._require_field("Provides")

    @property
    def description(self) -> str:
        return self._require_field("Description")

    @property
    def short_description(self) -> str:
        return self._require_field("_short_description")

    @property
    def long_description(self) -> str:
        return self._require_field("_long_description")


class Control:
    """Parse and manipulate a debian/control file."""

    _instance_id: int
    _perl_var: str

    def __init__(self) -> None:
        _ensure_loaded()
        self._instance_id = id(self)
        self._perl_var = f"$_control_{self._instance_id}"
        perlthon.eval(f"{self._perl_var} = Debian::Control->new()")

    def __del__(self) -> None:
        perl_var = getattr(self, "_perl_var", None)
        if perl_var is not None:
            try:
                perlthon.eval(f"undef {perl_var}")
            except Exception:
                pass

    @classmethod
    def from_file(cls, path: str | Path) -> Control:
        control = cls()
        resolved = str(Path(path))
        perlthon.eval(f"{control._perl_var}->read('{_escape(resolved)}')")
        return control

    @classmethod
    def from_string(cls, content: str) -> Control:
        control = cls()
        perlthon.eval(
            f"""do {{
                my $content = '{_escape(content)}';
                {control._perl_var}->read(\\$content);
            }}"""
        )
        return control

    @property
    def source(self) -> SourceStanza:
        return SourceStanza._from_expr(f"{self._perl_var}->source()")

    @property
    def binaries(self) -> list[BinaryStanza]:
        result = perlthon.eval(f"[{self._perl_var}->binary_tie()->Keys()]")
        if result is None:
            return []

        assert isinstance(result, list)
        binaries: list[BinaryStanza] = []
        for package in result:
            assert isinstance(package, str)
            binaries.append(
                BinaryStanza._from_expr(
                    f"{self._perl_var}->binary()->{{'{_escape(package)}'}}"
                )
            )
        return binaries

    def write(self, path: str | Path) -> None:
        perlthon.eval(f"{self._perl_var}->write('{_escape(str(Path(path)))}')")

    def to_string(self) -> str:
        result = perlthon.eval(
            f"""do {{
                my $content = '';
                {self._perl_var}->write(\\$content);
                $content;
            }}"""
        )
        assert isinstance(result, str)
        return result


__all__ = ["BinaryStanza", "Control", "SourceStanza", "Stanza"]
