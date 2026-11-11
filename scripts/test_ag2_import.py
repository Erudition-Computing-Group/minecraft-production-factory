import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agents.ag2_factory as f
print("AG2_AVAILABLE:", f.AG2_AVAILABLE)
print("Module loaded OK")
agents = f.create_agents()
print("Agents:", agents)
