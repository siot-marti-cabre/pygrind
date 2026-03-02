"""Tests for E1-S01: Initialize Project Structure."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestDirectoryStructure:
    """AC: src/pygrind/ directory exists with models/, core/, storage/, ui/ subpackages."""

    def test_src_pygrind_exists(self):
        assert (ROOT / "src" / "pygrind").is_dir()

    def test_models_subpackage(self):
        assert (ROOT / "src" / "pygrind" / "models" / "__init__.py").is_file()

    def test_core_subpackage(self):
        assert (ROOT / "src" / "pygrind" / "core" / "__init__.py").is_file()

    def test_storage_subpackage(self):
        assert (ROOT / "src" / "pygrind" / "storage" / "__init__.py").is_file()

    def test_ui_subpackage(self):
        assert (ROOT / "src" / "pygrind" / "ui" / "__init__.py").is_file()


class TestInitFiles:
    """AC: All __init__.py files created for package discovery."""

    def test_pygrind_init(self):
        assert (ROOT / "src" / "pygrind" / "__init__.py").is_file()

    def test_all_subpackages_have_init(self):
        for pkg in ["models", "core", "storage", "ui"]:
            init = ROOT / "src" / "pygrind" / pkg / "__init__.py"
            assert init.is_file(), f"Missing __init__.py in {pkg}/"


class TestPyprojectToml:
    """AC: pyproject.toml defines project metadata, dependencies, and dev dependencies."""

    def test_pyproject_exists(self):
        assert (ROOT / "pyproject.toml").is_file()

    def test_pyproject_has_project_metadata(self):
        content = (ROOT / "pyproject.toml").read_text()
        assert 'name = "pygrind"' in content
        assert 'version = "0.1.0"' in content
        assert 'requires-python = ">=3.10"' in content

    def test_pyproject_has_dependencies(self):
        content = (ROOT / "pyproject.toml").read_text()
        for dep in ["PyQt6", "QScintilla", "PyYAML", "platformdirs"]:
            assert dep in content, f"Missing dependency: {dep}"

    def test_pyproject_has_dev_dependencies(self):
        content = (ROOT / "pyproject.toml").read_text()
        for dep in ["pytest", "pytest-qt", "ruff", "pyinstaller"]:
            assert dep.lower() in content.lower(), f"Missing dev dependency: {dep}"


class TestEntryPoint:
    """AC: python -m pygrind runs without error."""

    def test_module_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "pygrind", "--version"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=10,
        )
        assert result.returncode == 0
        assert "PyGrind" in result.stdout
