import asyncio
from ag2 import Agent
from ag2.config import OllamaConfig

async def main():
    config = OllamaConfig(model="gemma4:latest", host="http://localhost:11434")
    agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
    async with agent.run("What is a particle in Minecraft?") as run:
        result = await run.result()
        print("Result type:", type(result))
        print("Result:", str(result)[:500])

asyncio.run(main())
