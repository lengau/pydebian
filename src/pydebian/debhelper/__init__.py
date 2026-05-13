"""Debhelper build system detection and sequence resolution.

Wraps Debian::Debhelper::Buildsystem, Debian::Debhelper::Dh_Buildsystems,
and debhelper sequence logic via perlthon.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import perlthon

# Build steps supported by debhelper
BUILD_STEPS = ("configure", "build", "test", "install", "clean")

# Buildsystems in debhelper's detection priority order
_BUILDSYSTEM_NAMES = (
    "autoconf",
    "perl_build",
    "perl_makemaker",
    "makefile",
    "python_distutils",
    "cmake",
    "ant",
    "qmake",
    "qmake6",
    "meson",
    "ninja",
    "pybuild",
)

_DH_LOADED = False


def _ensure_loaded() -> None:
    """Load debhelper buildsystem modules on first use."""
    global _DH_LOADED
    if not _DH_LOADED:
        perlthon.eval("use Debian::Debhelper::Buildsystem")
        names_str = " ".join(_BUILDSYSTEM_NAMES)
        perlthon.eval(f"""do {{
            for my $name (qw({names_str})) {{
                my $module = "Debian::Debhelper::Buildsystem::$name";
                eval "require $module";
            }}
        }}""")
        _DH_LOADED = True


@dataclass
class BuildSystem:
    """A debhelper build system."""

    name: str
    description: str
    is_generator: bool = False
    target_system: str | None = None

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"


def list_buildsystems() -> list[BuildSystem]:
    """List all known debhelper build systems.

    Returns the build systems in the order debhelper considers them
    for auto-detection.
    """
    _ensure_loaded()
    names_str = " ".join(_BUILDSYSTEM_NAMES)
    result = perlthon.eval(f"""do {{
        my @systems;
        for my $name (qw({names_str})) {{
            my $module = "Debian::Debhelper::Buildsystem::$name";
            eval "require $module";
            unless ($@) {{
                my $desc = eval {{ $module->DESCRIPTION() }} || "unknown";
                my $is_gen = eval {{ $module->IS_GENERATOR_BUILD_SYSTEM() }} || 0;
                push @systems, {{
                    name => $name,
                    description => $desc,
                    is_generator => $is_gen ? 1 : 0,
                }};
            }}
        }}
        \\@systems;
    }}""")

    systems = []
    assert isinstance(result, list)
    for s in result:
        assert isinstance(s, dict)
        systems.append(BuildSystem(
            name=str(s["name"]),
            description=str(s["description"]),
            is_generator=bool(s["is_generator"]),
        ))
    return systems


def detect_buildsystem(
    source_dir: str | Path,
    step: str = "configure",
) -> BuildSystem | None:
    """Auto-detect the build system for a source tree.

    Uses debhelper's auto-detection logic (checks for CMakeLists.txt,
    meson.build, configure, Makefile, etc.) in priority order.

    Args:
        source_dir: Path to the source tree root.
        step: Build step to check for (configure, build, test, install, clean).

    Returns:
        The detected BuildSystem, or None if no build system was detected.
    """
    if step not in BUILD_STEPS:
        raise ValueError(f"Invalid step {step!r}, must be one of {BUILD_STEPS}")

    _ensure_loaded()
    source_dir = str(Path(source_dir).resolve())
    escaped = source_dir.replace("\\", "\\\\").replace("'", "\\'")
    names_str = " ".join(_BUILDSYSTEM_NAMES)

    result = perlthon.eval(f"""do {{
        use Cwd;
        my $orig = getcwd();
        chdir('{escaped}') or die "Cannot chdir to {escaped}: $!";

        my $detected;
        for my $name (qw({names_str})) {{
            my $module = "Debian::Debhelper::Buildsystem::$name";
            eval "require $module";
            next if $@;
            my $bs = eval {{ $module->new(sourcedir => '.') }};
            next unless $bs;
            my $result = eval {{ $bs->check_auto_buildable('{step}') }};
            if ($result) {{
                $detected = {{
                    name => $bs->NAME(),
                    description => $bs->DESCRIPTION(),
                    is_generator => $bs->IS_GENERATOR_BUILD_SYSTEM() ? 1 : 0,
                }};
                last;
            }}
        }}

        chdir($orig);
        $detected;
    }}""")

    if result is None:
        return None

    assert isinstance(result, dict)
    return BuildSystem(
        name=str(result["name"]),
        description=str(result["description"]),
        is_generator=bool(result["is_generator"]),
    )


def get_compat_level(source_dir: str | Path | None = None) -> int | None:
    """Get the debhelper compatibility level for a source tree.

    Checks debian/compat file and Build-Depends for debhelper-compat
    virtual package.

    Args:
        source_dir: Path to the source tree (containing debian/ directory).
                   If None, uses current directory.

    Returns:
        The compat level as an integer, or None if not determinable.
    """
    if source_dir is not None:
        base = Path(source_dir)
    else:
        base = Path.cwd()

    # Check debian/compat file
    compat_file = base / "debian" / "compat"
    if compat_file.exists():
        content = compat_file.read_text().strip()
        if content.isdigit():
            return int(content)

    # Check Build-Depends for debhelper-compat (= N)
    control_file = base / "debian" / "control"
    if control_file.exists():
        import re

        content = control_file.read_text()
        match = re.search(r"debhelper-compat\s*\(\s*=\s*(\d+)\s*\)", content)
        if match:
            return int(match.group(1))

    return None


def get_sequence(target: str, source_dir: str | Path | None = None) -> list[str]:
    """Get the debhelper command sequence for a given build target.

    Must be run from (or pointed at) a source tree with debian/control
    and a debhelper compat level configured.

    Args:
        target: The debian/rules target (binary, build, clean, install, etc.).
        source_dir: Path to the source tree. If None, uses cwd.

    Returns:
        List of dh_* command names in execution order.
    """
    import json
    import subprocess

    valid_targets = (
        "binary", "binary-arch", "binary-indep",
        "build", "build-arch", "build-indep",
        "clean", "install", "install-arch", "install-indep",
    )
    if target not in valid_targets:
        raise ValueError(f"Invalid target {target!r}, must be one of {valid_targets}")

    cwd = str(Path(source_dir).resolve()) if source_dir else None

    # Try dh_assistant list-commands (returns all commands, not filtered)
    try:
        result = subprocess.run(
            ["dh_assistant", "list-commands", "--output-format=json"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "commands" in data:
                return [cmd["command"] for cmd in data["commands"]]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass

    # Fallback: list dh_* commands from system
    return get_dh_commands()


def get_dh_commands() -> list[str]:
    """Get a list of all available dh_* commands on the system."""
    import subprocess

    result = subprocess.run(
        ["find", "/usr/bin", "-name", "dh_*", "-executable"],
        capture_output=True,
        text=True,
    )
    commands = []
    for line in result.stdout.strip().split("\n"):
        if line:
            commands.append(Path(line).name)
    return sorted(commands)
