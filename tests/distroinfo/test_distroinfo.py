"""Tests for pydebian.distroinfo."""

import pytest

from pydebian.distroinfo import DebianDistroInfo, UbuntuDistroInfo


class TestUbuntuDistroInfo:
    @pytest.fixture
    def ubuntu(self):
        return UbuntuDistroInfo()

    def test_all_returns_list(self, ubuntu):
        all_releases = ubuntu.all()
        assert isinstance(all_releases, list)
        assert len(all_releases) > 10

    def test_all_contains_known_releases(self, ubuntu):
        all_releases = ubuntu.all()
        assert "noble" in all_releases
        assert "jammy" in all_releases
        assert "focal" in all_releases
        assert "bionic" in all_releases

    def test_stable(self, ubuntu):
        stable = ubuntu.stable()
        assert stable is not None
        assert isinstance(stable, str)
        assert len(stable) > 0

    def test_devel(self, ubuntu):
        devel = ubuntu.devel()
        assert devel is not None
        assert isinstance(devel, str)

    def test_lts(self, ubuntu):
        lts = ubuntu.lts()
        assert lts is not None
        assert isinstance(lts, str)

    def test_is_lts_true(self, ubuntu):
        # These are known LTS releases
        assert ubuntu.is_lts("noble") is True
        assert ubuntu.is_lts("jammy") is True
        assert ubuntu.is_lts("focal") is True

    def test_is_lts_false(self, ubuntu):
        # These are non-LTS
        assert ubuntu.is_lts("mantic") is False
        assert ubuntu.is_lts("lunar") is False

    def test_supported(self, ubuntu):
        supported = ubuntu.supported()
        assert isinstance(supported, list)
        assert len(supported) > 0
        # Current stable must be supported
        stable = ubuntu.stable()
        if stable:
            assert stable in supported

    def test_supported_esm(self, ubuntu):
        esm = ubuntu.supported_esm()
        assert isinstance(esm, list)
        # ESM includes LTS releases with extended support

    def test_valid_known(self, ubuntu):
        assert ubuntu.valid("noble") is True
        assert ubuntu.valid("jammy") is True

    def test_valid_unknown(self, ubuntu):
        assert ubuntu.valid("notarelease") is False

    def test_version(self, ubuntu):
        ver = ubuntu.version("noble")
        assert ver is not None
        assert "24.04" in ver

    def test_version_unknown(self, ubuntu):
        ver = ubuntu.version("notarelease")
        assert ver is None

    def test_unsupported(self, ubuntu):
        unsupported = ubuntu.unsupported()
        assert isinstance(unsupported, list)
        # Very old releases should be unsupported
        assert "warty" in unsupported


class TestDebianDistroInfo:
    @pytest.fixture
    def debian(self):
        return DebianDistroInfo()

    def test_all_returns_list(self, debian):
        all_releases = debian.all()
        assert isinstance(all_releases, list)
        assert len(all_releases) > 5

    def test_all_contains_known_releases(self, debian):
        all_releases = debian.all()
        assert "bookworm" in all_releases
        assert "bullseye" in all_releases
        assert "buster" in all_releases

    def test_stable(self, debian):
        stable = debian.stable()
        assert stable is not None
        assert isinstance(stable, str)

    def test_testing(self, debian):
        testing = debian.testing()
        assert testing is not None
        assert isinstance(testing, str)

    def test_devel(self, debian):
        devel = debian.devel()
        assert devel is not None
        assert isinstance(devel, str)

    def test_old(self, debian):
        old = debian.old()
        assert old is not None
        assert isinstance(old, str)

    def test_supported(self, debian):
        supported = debian.supported()
        assert isinstance(supported, list)
        assert len(supported) > 0
        # Stable must be in supported
        stable = debian.stable()
        if stable:
            assert stable in supported

    def test_supported_lts(self, debian):
        lts = debian.supported_lts()
        assert isinstance(lts, list)

    def test_supported_elts(self, debian):
        elts = debian.supported_elts()
        assert isinstance(elts, list)

    def test_valid_codenames(self, debian):
        assert debian.valid("bookworm") is True
        assert debian.valid("unstable") is True
        assert debian.valid("testing") is True
        assert debian.valid("stable") is True

    def test_valid_unknown(self, debian):
        assert debian.valid("notarelease") is False

    def test_codename_stable(self, debian):
        # "stable" should resolve to the current stable codename
        result = debian.codename("stable")
        assert result is not None
        assert result == debian.stable()

    def test_codename_testing(self, debian):
        result = debian.codename("testing")
        assert result is not None
        assert result == debian.testing()

    def test_version(self, debian):
        ver = debian.version("bookworm")
        assert ver is not None
        assert "12" in ver

    def test_unsupported(self, debian):
        unsupported = debian.unsupported()
        assert isinstance(unsupported, list)
        # Old releases should be unsupported
        assert "buzz" in unsupported or "woody" in unsupported
