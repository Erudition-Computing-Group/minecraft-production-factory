import inspect
from ag2 import Agent
from ag2.config import OllamaConfig

config = OllamaConfig(model="gemma4:12b", host="http://localhost:11434")
agent = Agent(name="Test", prompt="Answer in one sentence.", config=config)
run = agent.run("What is a particle in Minecraft?")
print("Run attrs:", [a for a in dir(run) if not a.startswith("_")])
print()
result = run.result
print("Result type:", type(result))
print("Result attrs:", [a for a in dir(result) if not a.startswith("_")])
print()
print("Result:", result)
# Try to get content
if hasattr(result, "content"):
    print("Content:", result.content)
if hasattr(result, "text"):
    print("Text:", result.text)
if hasattr(result, "message"):
    print("Message:", result.message)
if hasattr(result, "output"):
    print("Output:", result.output)
