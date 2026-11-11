import inspect
from ag2 import Agent
from ag2.config import OllamaConfig

print("run signature:", inspect.signature(Agent.run))
print()

# Create a simple agent and test
config = OllamaConfig(model="gemma4:12b", host="http://localhost:11434")
agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
result = agent.run("What is a particle in Minecraft?")
print("Result type:", type(result))
print("Result attrs:", [a for a in dir(result) if not a.startswith("_")])
print("Result:", result)
