"""Tests for pydebian.control."""

from __future__ import annotations

from pathlib import Path

from pydebian.control import BinaryStanza, Control, SourceStanza

CONTROL_TEXT = """Source: pydebian
Section: python
Priority: optional
Maintainer: Example Maintainer <maint@example.com>
Build-Depends: python3-all, debhelper-compat (= 13)
Standards-Version: 4.7.0
Homepage: https://example.com

Package: python3-pydebian
Architecture: all
Depends: ${misc:Depends}, ${python3:Depends}
Description: Python wrapper for Debian modules
 This is the long description.
 .
 Second paragraph.

Package: pydebian-doc
Architecture: all
Description: Documentation package
 Docs live here.
"""


class TestControl:
    def test_parse_from_string(self):
        control = Control.from_string(CONTROL_TEXT)

        assert isinstance(control.source, SourceStanza)
        assert control.source.source == "pydebian"
        assert control.source.maintainer == "Example Maintainer <maint@example.com>"
        assert control.source.build_depends == "python3-all, debhelper-compat (= 13)"

        binaries = control.binaries
        assert len(binaries) == 2
        assert all(isinstance(binary, BinaryStanza) for binary in binaries)
        assert binaries[0].package == "python3-pydebian"
        assert binaries[0].architecture == "all"
        assert binaries[0].depends == "${misc:Depends}, ${python3:Depends}"
        assert binaries[0].description.startswith("Python wrapper for Debian modules")
        assert binaries[1].package == "pydebian-doc"

    def test_parse_from_file(self, tmp_path: Path):
        control_path = tmp_path / "control"
        control_path.write_text(CONTROL_TEXT)

        control = Control.from_file(control_path)

        assert control.source.homepage == "https://example.com"
        assert [binary.package for binary in control.binaries] == [
            "python3-pydebian",
            "pydebian-doc",
        ]

    def test_stanza_field_access(self):
        control = Control.from_string(CONTROL_TEXT)
        source = control.source

        assert source["Source"] == "pydebian"
        assert source["Homepage"] == "https://example.com"
        assert "Maintainer" in source
        assert "XS-Autobuild" not in source
        assert source.keys() == [
            "Source",
            "Section",
            "Priority",
            "Maintainer",
            "Build-Depends",
            "Standards-Version",
            "Homepage",
        ]
        assert (
            "Maintainer",
            "Example Maintainer <maint@example.com>",
        ) in source.items()

    def test_missing_fields(self):
        control = Control.from_string(CONTROL_TEXT)
        second_binary = control.binaries[1]

        assert second_binary["Depends"] is None
        assert "Depends" not in second_binary

    def test_modify_fields(self):
        control = Control.from_string(CONTROL_TEXT)

        control.source["Maintainer"] = "Updated Maintainer <updated@example.com>"
        control.binaries[1]["Depends"] = "python3"

        assert control.source.maintainer == "Updated Maintainer <updated@example.com>"
        assert control.binaries[1].depends == "python3"

    def test_write_and_round_trip(self, tmp_path: Path):
        control = Control.from_string(CONTROL_TEXT)
        output_path = tmp_path / "debian.control"

        control.source["Build-Depends"] = (
            "zlib1g-dev, debhelper-compat (= 13), python3-all"
        )
        control.write(output_path)

        written = output_path.read_text()
        reloaded = Control.from_file(output_path)

        assert (
            "Build-Depends: debhelper-compat (= 13), python3-all, zlib1g-dev" in written
        )
        assert (
            reloaded.source.build_depends
            == "debhelper-compat (= 13), python3-all, zlib1g-dev"
        )
        assert [binary.package for binary in reloaded.binaries] == [
            "python3-pydebian",
            "pydebian-doc",
        ]

    def test_to_string_round_trip_consistency(self):
        control = Control.from_string(CONTROL_TEXT)

        serialized = control.to_string()
        reparsed = Control.from_string(serialized)

        assert reparsed.source.source == control.source.source
        assert reparsed.source.build_depends == control.source.build_depends
        assert [binary.package for binary in reparsed.binaries] == [
            binary.package for binary in control.binaries
        ]
        assert reparsed.binaries[0].description == control.binaries[0].description

    def test_binary_stanza_iteration(self):
        control = Control.from_string(CONTROL_TEXT)

        packages = [binary.package for binary in control.binaries]

        assert packages == ["python3-pydebian", "pydebian-doc"]

    def test_binary_description_helpers(self):
        control = Control.from_string(CONTROL_TEXT)
        binary = control.binaries[0]

        assert binary.short_description == "Python wrapper for Debian modules"
        assert (
            binary.long_description
            == "This is the long description.\n\nSecond paragraph."
        )
