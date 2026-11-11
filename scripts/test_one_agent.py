import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.ag2_factory import create_agents

async def main():
    agents = create_agents()
    print("Agents:", list(agents.keys()))
    
    # Test just the concept agent
    async with agents["concept"].run("What is a particle effect in Minecraft? Answer in one sentence.") as run:
        result = await run.result()
    print("Concept response:", result.body[:300])

asyncio.run(main())
print("DONE")
