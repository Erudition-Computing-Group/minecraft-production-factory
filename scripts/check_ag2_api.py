import ag2
print("ag2 version:", getattr(ag2, "__version__", "unknown"))
print()
# List all public names
names = [n for n in dir(ag2) if not n.startswith("_")]
print("Public names:", names)
print()
# Check submodules
import ag2.agentchat as ac
print("agentchat names:", [n for n in dir(ac) if "Agent" in n or "Group" in n])
