from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def test_development_bedrock_pack_validates_and_packages(tmp_path):
    output = tmp_path / "minecraft-production-factory.mcpack"
    result = subprocess.run(
        [sys.executable, "scripts/bedrock_pack.py", "--output", str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert output.is_file()


def test_golden_treasure_spec_conforms_to_the_concept_schema():
    import json
    from jsonschema import validate

    schema = json.loads((ROOT / "agents/schemas/concept_spec.schema.json").read_text())
    spec = json.loads((ROOT / "config/effects/golden_treasure_sparkle.bedrock.json").read_text())
    validate(spec, schema)
