"""Orchestrator: drives a batch of particle ideas through the 5-agent pipeline."""
import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY = ROOT / "memory" / "episodic" / "active_runs"
LOGS = ROOT / "logs" / "agent_traces"


def load_batch(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def new_run_id():
    return "batch-" + uuid.uuid4().hex[:8]


def log_event(run_id, agent, payload):
    LOGS.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "agent": agent,
        **payload,
    }
    out = LOGS / f"{run_id}.jsonl"
    with open(out, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


def persist_state(run_id, state):
    MEMORY.mkdir(parents=True, exist_ok=True)
    path = MEMORY / f"{run_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    return path


def run_batch(batch_path):
    batch = load_batch(batch_path)
    run_id = new_run_id()
    state = {"run_id": run_id, "ideas": batch.get("ideas", []), "stages": {}}
    log_event(run_id, "orchestrator", {"event": "batch_started", "count": len(state["ideas"])})
    # Stage hooks are intentionally thin: each agent module implements its own logic.
    # The orchestrator persists state so a failed run can be resumed.
    persist_state(run_id, state)
    log_event(run_id, "orchestrator", {"event": "batch_state_persisted", "path": str(MEMORY / f"{run_id}.json")})
    print(f"Run {run_id} initialized with {len(state['ideas'])} ideas.")
    print("Next: invoke Concept & Spec Agent per idea (see agents/concept_agent.py).")
    return run_id


def main():
    parser = argparse.ArgumentParser(description="Particle Effects Factory orchestrator")
    parser.add_argument("--batch", required=True, help="Path to a batch JSON file (e.g. config/batch_01.json)")
    args = parser.parse_args()
    run_batch(args.batch)


if __name__ == "__main__":
    main()
