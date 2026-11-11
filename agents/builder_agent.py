"""Builder Agent: writes production Java/PaperMC or Bedrock .particle.json files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "agents" / "prompts" / "builder_agent.md"


def system_prompt():
    return PROMPT.read_text(encoding="utf-8")


def output_path(slug, edition="java"):
    if edition == "java":
        return ROOT / "src" / "java_plugins" / f"{slug}.java"
    return ROOT / "src" / "bedrock_addons" / f"{slug}.particle.json"
