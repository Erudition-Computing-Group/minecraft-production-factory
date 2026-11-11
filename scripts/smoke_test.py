import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agents.orchestrator, agents.math_agent, agents.concept_agent
print("imports ok")
from agents.math_agent import verify_bounding_box
print(verify_bounding_box("def coords(t):\n    return (1.0, 0.0, 0.0)", ticks=5, radius=3.0))
