import asyncio
from ag2 import Agent
from ag2.config import OllamaConfig

async def main():
    config = OllamaConfig(model="gemma4:12b", host="http://localhost:11434")
    agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
    run = agent.run("What is a particle in Minecraft?")
    result = await run.result()
    print("Result type:", type(result))
    print("Result:", result)
    if hasattr(result, "__dict__"):
        print("Attrs:", list(result.__dict__.keys()))
    print("Str:", str(result)[:500])

asyncio.run(main())
