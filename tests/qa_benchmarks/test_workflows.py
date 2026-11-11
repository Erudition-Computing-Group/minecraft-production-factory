"""Validate GitHub Actions workflow YAML files."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


def test_workflows_exist():
    expected = ["ci.yml", "release.yml", "factory-run.yml", "nightly.yml", "codeql.yml"]
    for name in expected:
        path = WORKFLOWS / name
        assert path.exists(), f"Missing workflow: {name}"


def test_workflows_valid_yaml():
    try:
        import yaml
    except ImportError:
        print("PyYAML not installed, skipping YAML validation")
        return
    for path in WORKFLOWS.glob("*.yml"):
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"Empty workflow: {path.name}"
        assert "jobs" in data, f"No jobs in: {path.name}"
        assert "name" in data, f"No name in: {path.name}"


def test_dependabot_exists():
    assert (ROOT / ".github" / "dependabot.yml").exists()


def test_issue_templates_exist():
    templates = ROOT / ".github" / "ISSUE_TEMPLATE"
    expected = ["spec.md", "math.md", "build.md", "qa-fail.md",
                "visual-review.md", "release.md"]
    for name in expected:
        assert (templates / name).exists(), f"Missing template: {name}"
