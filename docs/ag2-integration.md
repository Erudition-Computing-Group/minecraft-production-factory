# AG2 (AutoGen) Integration Plan

## Why AG2?

AG2 (formerly AutoGen) is a multi-agent framework that provides:
- **Conversational agents** with built-in LLM integration
- **Group chat** for multi-agent collaboration (Spec → Math → Build → QA → Review)
- **Tool use** — register Python interpreter, shell, file I/O as agent tools
- **Code execution** — agents can write and run code
- **Human-in-the-loop** — UserProxyAgent for visual review gate
- **Structured output** — JSON schema enforcement for agent responses

This replaces our stub orchestrator with a real multi-agent conversation system.

## AG2 vs. Current Architecture

| Current | With AG2 |
|---------|----------|
| Stub Python modules with placeholder functions | Real LLM-powered agents with system prompts |
| Manual state persistence (JSON files) | AG2 manages conversation history |
| No actual LLM calls | Agents call LLMs via AG2's AssistantAgent |
| No tool use | Math Agent gets Python interpreter, QA Agent gets shell |
| No feedback loop | GroupChatManager handles Builder↔QA retry loops |
| Manual issue creation | Agents can call GitHub API as a tool |

## Agent Mapping

| Factory Agent | AG2 Class | Tools | Model |
|--------------|-----------|-------|-------|
| Concept & Spec | `AssistantAgent` | JSON schema validator | Fast (Gemma 4 12B) |
| Math & Geometry | `AssistantAgent` | Python interpreter (numpy) | Reasoning (Qwen 3 27B) |
| Builder | `AssistantAgent` | File writer | Coding (Devstral) |
| QA & Performance | `AssistantAgent` | Shell (gradle, linter) | Reasoning (GPT-OSS 20B) |
| Storefront & Ops | `AssistantAgent` | GitHub API (issues, PRs) | Fast (Gemma 4 12B) |
| Human (Visual Review) | `UserProxyAgent` | Terminal input | Human |

## AG2 Conversation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    GroupChat (Factory Floor)                 │
│                                                             │
│  ConceptAgent → "Here's the spec for Cybernetic Wings"       │
│       ↓                                                     │
│  MathAgent → "Here are the verified (x,y,z) formulas"       │
│       ↓                                                     │
│  BuilderAgent → "Java class written to feature/cybernetic"   │
│       ↓                                                     │
│  QAAgent → runs gradle build → "BUILD FAILED: missing import"│
│       ↓ (retry)                                             │
│  BuilderAgent → "Fixed import, re-committed"                │
│       ↓                                                     │
│  QAAgent → "BUILD SUCCESS, MSPT 12ms, 0 errors"             │
│       ↓                                                     │
│  HumanProxy → "Visual check: looks good, approved"           │
│       ↓                                                     │
│  StorefrontAgent → "Created [RELEASE] issue, Tebex cmd ready"│
└─────────────────────────────────────────────────────────────┘
```

## Implementation Plan

### Phase 1: Add AG2 dependency
- Add `ag2` (or `autogen`) to requirements.txt
- Configure LLM endpoints (Ollama for local, or cloud API)

### Phase 2: AG2 Agent definitions
- Create `agents/ag2_factory.py` with AG2 agent instances
- Map system prompts from `agents/prompts/*.md`
- Register tools (Python interpreter, shell, file writer, GitHub API)

### Phase 3: Group chat orchestration
- Replace `orchestrator.py` with AG2 GroupChatManager
- Configure speaker selection (sequential or auto)
- Add termination conditions (max rounds, human approval)

### Phase 4: Human-in-the-loop
- UserProxyAgent for visual review gate
- Pause conversation for human input
- Resume after approval/rejection

### Phase 5: GitHub integration
- Register GitHub API as an agent tool
- Agents create issues, PRs, and comments automatically
- No need for separate `create_issues.py` script

## AG2 Configuration

```python
import autogen

# LLM config for local Ollama
llm_config = {
    "config_list": [
        {"model": "gemma4:12b", "base_url": "http://localhost:11434/v1", "api_key": "ollama"},
    ],
    "temperature": 0.7,
}

# Or cloud config
llm_config_cloud = {
    "config_list": [
        {"model": "claude-sonnet-4-20250514", "api_key": os.environ["ANTHROPIC_API_KEY"]},
    ],
}
```

## Tool Registration

```python
# Math Agent gets Python interpreter
math_agent = AssistantAgent(
    name="MathAgent",
    system_message=open("agents/prompts/math_agent.md").read(),
    llm_config=llm_config_reasoning,
    code_execution_config={"use_docker": False},  # or True for safety
)

# QA Agent gets shell access
qa_agent = AssistantAgent(
    name="QAAgent",
    system_message=open("agents/prompts/qa_agent.md").read(),
    llm_config=llm_config,
    # Tools registered via function calling
)
```

## Key AG2 Features We'd Use

1. **`code_execution_config`** — Math Agent runs Python to verify formulas
2. **`function_map`** — Register custom tools (GitHub API, file writer)
3. **`GroupChat`** — Multi-agent conversation with speaker selection
4. **`max_round`** — Limit conversation length to prevent infinite loops
5. **`human_input_mode`** — "ALWAYS" for visual review, "NEVER" for automated stages
6. **`reflect_on_tool_use`** — Agents analyze tool results before responding
7. **`description`** — Agent descriptions for auto speaker selection

## Dependencies

```txt
ag2>=0.4.0  # or autogen>=0.2.0 for older API
```

## Migration Path

1. Keep existing Python modules as-is (they work for testing)
2. Add AG2 agents alongside (new `agents/ag2_*.py` files)
3. Update orchestrator to use AG2 GroupChat when LLM is available
4. Fall back to stub mode when no LLM configured
5. Gradually migrate all agents to AG2

## References
- AG2 docs: https://docs.ag2.ai/
- AG2 GitHub: https://github.com/ag2ai/ag2
- AutoGen original: https://microsoft.github.io/autogen/