"""QA & Performance Agent: compiles, lints, stress-tests TPS/MSPT."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "agents" / "prompts" / "qa_agent.md"


def system_prompt():
    return PROMPT.read_text(encoding="utf-8")


def performance_gate(mspt, max_mspt=50.0, tps=20.0, target_tps=20.0):
    return mspt < max_mspt and tps >= target_tps
