"""Simple test runner (no pytest needed)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Import test modules
import importlib.util

test_files = [
    "tests/qa_benchmarks/test_schemas.py",
    "tests/qa_benchmarks/test_math_bounds.py",
    "tests/qa_benchmarks/test_particles.py",
]

passed = 0
failed = 0
for tf in test_files:
    path = Path(__file__).resolve().parents[1] / tf
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    # patch sys.path for imports inside test files
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    # find test functions
    for name in dir(mod):
        if name.startswith("test_"):
            fn = getattr(mod, name)
            if callable(fn):
                try:
                    fn()
                    print(f"  PASS  {tf}::{name}")
                    passed += 1
                except Exception as e:
                    print(f"  FAIL  {tf}::{name}: {e}")
                    failed += 1

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
