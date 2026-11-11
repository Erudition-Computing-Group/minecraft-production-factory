"""Test AG2 1.3.1 simple agent creation."""
import ag2
from ag2 import Agent
from ag2.config import OllamaConfig

# Create Ollama config
config = OllamaConfig(
    model="gemma4:12b",
    host="http://localhost:11434",
)

# Create agent
agent = Agent(
    name="TestAgent",
    prompt="You are a helpful assistant. Answer concisely.",
    config=config,
)

print(f"Agent created: {agent.name}")
print("Success!")
