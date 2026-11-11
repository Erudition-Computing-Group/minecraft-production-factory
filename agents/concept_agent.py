"""Concept & Spec Agent: turns a raw idea into a structured JSON spec."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "agents" / "schemas" / "concept_spec.schema.json"
PROMPT = ROOT / "agents" / "prompts" / "concept_agent.md"


def load_schema():
    with open(SCHEMA, encoding="utf-8") as f:
        return json.load(f)


def system_prompt():
    return PROMPT.read_text(encoding="utf-8")


def build_spec(idea, edition="java"):
    """Placeholder: an LLM call would fill this using system_prompt() + schema.

    Returns a dict conforming to concept_spec.schema.json.
    """
    return {
        "theme": idea,
        "edition": edition,
        "particle_types": ["END_ROD", "DUST"],
        "colors": {"primary": [0, 200, 255], "secondary": [255, 255, 255]},
        "animation_style": "flapping",
        "budget": {"max_particles_per_tick": 120, "culling_radius_blocks": 32},
        "compliance": "cosmetic-only (no hitboxes, buffs, or pay-to-win)",
    }
