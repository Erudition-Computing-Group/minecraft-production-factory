import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agents.ag2_factory as f
print("AG2_AVAILABLE:", f.AG2_AVAILABLE)
agents = f.create_agents()
print("Agents created:", list(agents.keys()) if agents else None)
# Test a single agent run (if Ollama is running)
try:
    resp = agents["concept"].run("What is a particle effect in Minecraft? Answer in one sentence.")
    print("Concept response:", resp.content[:200])
except Exception as e:
    print("Agent run failed (Ollama may not be running):", e)
