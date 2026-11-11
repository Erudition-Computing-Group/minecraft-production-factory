import asyncio
from ag2 import Agent
from ag2.config import OllamaConfig

async def main():
    config = OllamaConfig(model="gemma4:latest", host="http://localhost:11434")
    agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
    async with agent.run("What is a particle in Minecraft?") as run:
        result = await run.result()
        print("content type:", type(result.content))
        print("content:", result.content())
        print("body:", result.body if hasattr(result, "body") else "N/A")
        print("response:", result.response if hasattr(result, "response") else "N/A")

asyncio.run(main())
