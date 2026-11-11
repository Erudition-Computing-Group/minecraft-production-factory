import inspect
from ag2 import Agent
from ag2.config import OllamaConfig

config = OllamaConfig(model="gemma4:12b", host="http://localhost:11434")
agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
run = agent.run("What is a particle in Minecraft?")
print("Result method:", run.result)
print("Type:", type(run.result()))
# Let's try calling it
r = run.result()
print("Result:", r)
print("Type of r:", type(r))
if hasattr(r, "__dict__"):
    print("Attrs:", list(r.__dict__.keys()))
print("Str:", str(r)[:500])
