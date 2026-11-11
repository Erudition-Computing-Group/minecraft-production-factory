"""Math & Geometry Agent: solves 3D spatial math and verifies with Python."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "agents" / "prompts" / "math_agent.md"


def system_prompt():
    return PROMPT.read_text(encoding="utf-8")


def verify_bounding_box(formulas_py, ticks=80, radius=3.0):
    """Run the Math Agent's formulas in a sandboxed exec and assert bounds.

    formulas_py: a string of Python defining a function `coords(t)` returning (x,y,z).
    Returns (ok, message).
    """
    import math as _math
    safe_builtins = {
        "abs": abs, "min": min, "max": max, "round": round,
        "range": range, "len": len, "float": float, "int": int,
        "math": _math, "__import__": __import__,
    }
    ns = {}
    try:
        exec(formulas_py, {"__builtins__": safe_builtins}, ns)  # noqa: S102
    except Exception as e:
        return False, f"exec failed: {e}"
    coords = ns.get("coords")
    if not callable(coords):
        return False, "no coords(t) function defined"
    import math
    for t in range(ticks):
        x, y, z = coords(t)
        if any(v != v for v in (x, y, z)):  # NaN check
            return False, f"NaN at t={t}"
        if any(abs(v) == float("inf") for v in (x, y, z)):
            return False, f"Inf at t={t}"
        if (x * x + y * y + z * z) ** 0.5 > radius:
            return False, f"out of bounds at t={t}: ({x},{y},{z})"
    return True, "bounding box OK"
