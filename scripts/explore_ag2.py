import ag2
from ag2 import Agent, Task, TaskConfig, TaskSpec, Toolkit, ToolResult
import inspect

# Check Agent class
print("=== Agent class ===")
print(inspect.signature(Agent.__init__))
print()

# Check Task class
print("=== Task class ===")
print(inspect.signature(Task.__init__))
print()

# Check how to create an LLM agent
print("=== Agent module ===")
import ag2.agent as agent_mod
print([n for n in dir(agent_mod) if not n.startswith("_")])
print()

# Check for LLM config
print("=== Config ===")
import ag2.config as config_mod
print([n for n in dir(config_mod) if not n.startswith("_")])
print()

# Check tools
print("=== Tools ===")
import ag2.tools as tools_mod
print([n for n in dir(tools_mod) if not n.startswith("_")][:30])
print()

# Check if there's an AssistantAgent equivalent
for name in ["AssistantAgent", "UserProxyAgent", "GroupChat", "GroupChatManager"]:
    if hasattr(ag2, name):
        print(f"FOUND: {name}")
    else:
        print(f"MISSING: {name}")
