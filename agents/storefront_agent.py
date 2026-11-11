"""Storefront & Ops Agent: packages releases and writes marketplace listings."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "agents" / "prompts" / "storefront_agent.md"


def system_prompt():
    return PROMPT.read_text(encoding="utf-8")


def tebex_delivery_command(permission_node):
    return f"/lp user {{name}} permission set {permission_node} true"
