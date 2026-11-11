"""AG2 (AutoGen) agent factory for the Particle Effects Factory.

Uses AG2 1.3.1 API: Agent, async run(), OllamaConfig.

Usage:
    python -m agents.ag2_factory --demo
"""
import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PROMPTS_DIR = ROOT / "agents" / "prompts"

# Try to import AG2
AG2_AVAILABLE = False
try:
    import ag2
    from ag2 import Agent
    from ag2.config import OllamaConfig
    AG2_AVAILABLE = True
except ImportError:
    pass


def _load_prompt(name):
    path = PROMPTS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"You are the {name} agent."


def get_llm_config(model="gemma4:latest", host=None):
    """Build AG2 OllamaConfig."""
    if host is None:
        host = os.environ.get("LLM_HOST", "http://localhost:11434")
    return OllamaConfig(model=model, host=host)


def create_agents(fast_model="gemma4:latest", reasoning_model="gemma4:latest",
                  coding_model="gemma4:latest", host=None):
    """Create all 5 factory agents.

    Returns dict of agent name -> Agent instance.
    """
    if not AG2_AVAILABLE:
        print("AG2 not installed. Install with: pip install 'ag2[ollama]'")
        return None

    agents = {}

    agents["concept"] = Agent(
        name="ConceptSpecAgent",
        prompt=_load_prompt("concept_agent"),
        config=get_llm_config(fast_model, host),
    )

    agents["math"] = Agent(
        name="MathGeometryAgent",
        prompt=_load_prompt("math_agent"),
        config=get_llm_config(reasoning_model, host),
    )

    agents["builder"] = Agent(
        name="BuilderAgent",
        prompt=_load_prompt("builder_agent"),
        config=get_llm_config(coding_model, host),
    )

    agents["qa"] = Agent(
        name="QAPerformanceAgent",
        prompt=_load_prompt("qa_agent"),
        config=get_llm_config(reasoning_model, host),
    )

    agents["storefront"] = Agent(
        name="StorefrontOpsAgent",
        prompt=_load_prompt("storefront_agent"),
        config=get_llm_config(fast_model, host),
    )

    return agents


async def run_factory_batch(ideas, fast_model="gemma4:latest", reasoning_model="gemma4:latest",
                            coding_model="gemma4:latest", host=None):
    """Run a batch of ideas through the AG2 factory pipeline."""
    if not AG2_AVAILABLE:
        print("AG2 not available. Install with: pip install 'ag2[ollama]'")
        return

    agents = create_agents(fast_model=fast_model, reasoning_model=reasoning_model,
                           coding_model=coding_model, host=host)
    if agents is None:
        return

    for idea in ideas:
        print(f"\n{'='*60}")
        print(f"Processing: {idea}")
        print(f"{'='*60}\n")

        print("[1/5] Concept & Spec Agent...")
        async with agents["concept"].run(
            f"Create a particle effect spec for: {idea}. Output JSON only."
        ) as run:
            spec_response = await run.result()
        print(f"  Spec: {spec_response.body[:300]}")

        print("[2/5] Math & Geometry Agent...")
        async with agents["math"].run(
            f"Given this spec, solve the 3D math: {spec_response.body}"
        ) as run:
            math_response = await run.result()
        print(f"  Math: {math_response.body[:300]}")

        print("[3/5] Builder Agent...")
        async with agents["builder"].run(
            f"Write Java code for: {idea}. Math: {math_response.body}"
        ) as run:
            build_response = await run.result()
        print(f"  Build: {build_response.body[:300]}")

        print("[4/5] QA & Performance Agent...")
        async with agents["qa"].run(
            f"Review this code for quality: {build_response.body}"
        ) as run:
            qa_response = await run.result()
        print(f"  QA: {qa_response.body[:300]}")

        print("[5/5] Storefront & Ops Agent...")
        async with agents["storefront"].run(
            f"Create store listing for: {idea}. Spec: {spec_response.body}"
        ) as run:
            store_response = await run.result()
        print(f"  Store: {store_response.body[:300]}")

    print("\nFactory batch complete.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AG2 Particle Factory")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample ideas")
    parser.add_argument("--idea", type=str, help="Single idea to process")
    parser.add_argument("--model", default="gemma4:latest", help="LLM model name")
    parser.add_argument("--host", default=None, help="LLM host URL")
    args = parser.parse_args()

    if not AG2_AVAILABLE:
        print("AG2 is not installed.")
        print("Install with: pip install 'ag2[ollama]'")
        sys.exit(1)

    if args.demo:
        asyncio.run(run_factory_batch(["Cybernetic Wings"]))
    elif args.idea:
        asyncio.run(run_factory_batch([args.idea], fast_model=args.model, host=args.host))
    else:
        print("Use --demo or --idea 'Effect Name'")
        print("Example: python -m agents.ag2_factory --demo")


if __name__ == "__main__":
    main()
