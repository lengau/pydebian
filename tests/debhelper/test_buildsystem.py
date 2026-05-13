"""Tests for pydebian.debhelper build system detection."""

import pytest

from pydebian.debhelper import (
    BUILD_STEPS,
    detect_buildsystem,
    get_compat_level,
    get_dh_commands,
    get_sequence,
    list_buildsystems,
)


class TestListBuildsystems:
    def test_returns_list(self):
        systems = list_buildsystems()
        assert isinstance(systems, list)
        assert len(systems) > 0

    def test_contains_known_systems(self):
        systems = list_buildsystems()
        names = [s.name for s in systems]
        # These should always be present
        assert "makefile" in names
        assert "autoconf" in names

    def test_buildsystem_has_description(self):
        systems = list_buildsystems()
        for s in systems:
            assert s.name
            assert s.description
            assert isinstance(s.is_generator, bool)

    def test_meson_is_generator(self):
        systems = list_buildsystems()
        meson_systems = [s for s in systems if "meson" in s.name]
        for s in meson_systems:
            assert s.is_generator


class TestDetectBuildsystem:
    def test_detect_meson(self, tmp_path):
        (tmp_path / "meson.build").write_text("project('test', 'c')\n")
        bs = detect_buildsystem(tmp_path)
        assert bs is not None
        assert "meson" in bs.name

    def test_detect_cmake(self, tmp_path):
        (tmp_path / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 3.10)\n"
        )
        bs = detect_buildsystem(tmp_path)
        assert bs is not None
        assert "cmake" in bs.name

    def test_detect_autoconf(self, tmp_path):
        configure = tmp_path / "configure"
        configure.write_text("#!/bin/sh\n")
        configure.chmod(0o755)
        bs = detect_buildsystem(tmp_path)
        assert bs is not None
        assert "autoconf" in bs.name

    def test_detect_makefile(self, tmp_path):
        (tmp_path / "Makefile").write_text("all:\n\techo hello\n")
        bs = detect_buildsystem(tmp_path)
        assert bs is not None
        assert "makefile" in bs.name

    def test_detect_none(self, tmp_path):
        # Empty directory - no build system
        bs = detect_buildsystem(tmp_path)
        assert bs is None

    def test_invalid_step(self, tmp_path):
        with pytest.raises(ValueError):
            detect_buildsystem(tmp_path, step="invalid")

    def test_all_steps_valid(self, tmp_path):
        (tmp_path / "meson.build").write_text("project('test', 'c')\n")
        for step in BUILD_STEPS:
            # Should not raise
            detect_buildsystem(tmp_path, step=step)


class TestGetCompatLevel:
    def test_from_compat_file(self, tmp_path):
        debian = tmp_path / "debian"
        debian.mkdir()
        (debian / "compat").write_text("13\n")
        level = get_compat_level(tmp_path)
        assert level == 13

    def test_no_compat(self, tmp_path):
        debian = tmp_path / "debian"
        debian.mkdir()
        level = get_compat_level(tmp_path)
        # Could be None if no compat info found
        assert level is None or isinstance(level, int)

    def test_from_build_depends(self, tmp_path):
        debian = tmp_path / "debian"
        debian.mkdir()
        (debian / "control").write_text(
            "Source: test\n"
            "Build-Depends: debhelper-compat (= 14)\n\n"
            "Package: test\nArchitecture: all\n"
        )
        level = get_compat_level(tmp_path)
        assert level == 14


class TestGetSequence:
    def test_invalid_target(self):
        with pytest.raises(ValueError):
            get_sequence("invalid")

    def test_binary_in_source_tree(self, tmp_path):
        """When run in a proper source tree, should return commands."""
        debian = tmp_path / "debian"
        debian.mkdir()
        (debian / "control").write_text(
            "Source: test\n"
            "Build-Depends: debhelper-compat (= 13)\n\n"
            "Package: test\nArchitecture: all\nDescription: test\n"
        )
        (debian / "changelog").write_text(
            "test (1.0-1) unstable; urgency=low\n\n"
            "  * Initial.\n\n"
            " -- Test <t@t.com>  Mon, 01 Jan 2024 00:00:00 +0000\n"
        )
        result = get_sequence("binary", source_dir=tmp_path)
        assert isinstance(result, list)
        assert len(result) > 0
        # Should contain dh_* commands
        assert all(cmd.startswith("dh_") for cmd in result)


class TestGetDhCommands:
    def test_returns_list(self):
        commands = get_dh_commands()
        assert isinstance(commands, list)
        assert len(commands) > 0

    def test_contains_known_commands(self):
        commands = get_dh_commands()
        assert "dh_install" in commands
        assert "dh_compress" in commands
        assert "dh_gencontrol" in commands
        assert "dh_auto_build" in commands

    def test_sorted(self):
        commands = get_dh_commands()
        assert commands == sorted(commands)
