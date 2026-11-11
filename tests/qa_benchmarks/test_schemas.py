import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "agents" / "schemas" / "concept_spec.schema.json"
BUDGETS = ROOT / "config" / "particle_budgets.json"


def test_schema_loads():
    with open(SCHEMA, encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["title"] == "Concept & Spec"


def test_budgets_under_cap():
    with open(BUDGETS, encoding="utf-8") as f:
        b = json.load(f)
    assert b["max_particles_per_tick"] <= 150
    assert b["max_mspt"] <= 50
