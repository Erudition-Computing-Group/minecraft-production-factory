#!/usr/bin/env python3
"""Validate and package the Bedrock development resource pack.

This intentionally uses only the Python standard library so it can run locally
and in GitHub Actions before optional Creator Tools validation is introduced.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = ROOT / "src" / "bedrock_addons" / "resource_pack"
IDENTIFIER = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
MAX_INSTANT_PARTICLES = 200
MAX_STEADY_PARTICLES_PER_SECOND = 200


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as source:
            value = json.load(source)
    except json.JSONDecodeError as error:
        fail(f"{path}: invalid JSON: {error.msg} (line {error.lineno})")
    if not isinstance(value, dict):
        fail(f"{path}: expected a JSON object")
    return value


def validate_manifest(pack: Path) -> None:
    manifest = load_json(pack / "manifest.json")
    header = manifest.get("header", {})
    modules = manifest.get("modules", [])
    if manifest.get("format_version") != 2:
        fail("manifest.json: format_version must be 2")
    for field in ("name", "description", "uuid", "version", "min_engine_version"):
        if field not in header:
            fail(f"manifest.json: header.{field} is required")
    if not isinstance(modules, list) or not any(m.get("type") == "resources" for m in modules if isinstance(m, dict)):
        fail("manifest.json: must declare a resources module")


def validate_particle(path: Path, pack: Path, seen_identifiers: set[str]) -> None:
    document = load_json(path)
    effect = document.get("particle_effect", {})
    description = effect.get("description", {}) if isinstance(effect, dict) else {}
    identifier = description.get("identifier")
    if document.get("format_version") is None or not isinstance(effect, dict):
        fail(f"{path}: requires format_version and particle_effect")
    if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
        fail(f"{path}: identifier must be a lowercase namespace:name")
    if identifier.startswith("minecraft:"):
        fail(f"{path}: minecraft: is reserved; use your own namespace")
    if identifier in seen_identifiers:
        fail(f"{path}: duplicate particle identifier {identifier}")
    seen_identifiers.add(identifier)

    render = description.get("basic_render_parameters", {})
    texture = render.get("texture") if isinstance(render, dict) else None
    if not isinstance(texture, str) or not render.get("material"):
        fail(f"{path}: basic_render_parameters requires material and texture")
    # Bedrock's built-in particle atlas is intentionally not shipped in a pack.
    texture_file = pack / f"{texture}.png"
    if texture != "textures/particle/particles" and not texture_file.is_file():
        fail(f"{path}: missing texture {texture_file.relative_to(pack)}")

    components = effect.get("components", {})
    if not isinstance(components, dict):
        fail(f"{path}: components must be an object")
    instant = components.get("minecraft:emitter_rate_instant", {})
    if isinstance(instant, dict) and instant.get("num_particles", 0) > MAX_INSTANT_PARTICLES:
        fail(f"{path}: instant emitter exceeds {MAX_INSTANT_PARTICLES} particles")
    steady = components.get("minecraft:emitter_rate_steady", {})
    if isinstance(steady, dict) and steady.get("spawn_rate", 0) > MAX_STEADY_PARTICLES_PER_SECOND:
        fail(f"{path}: steady emitter exceeds {MAX_STEADY_PARTICLES_PER_SECOND} particles/sec")


def validate(pack: Path) -> list[Path]:
    if not pack.is_dir():
        fail(f"resource pack directory does not exist: {pack}")
    validate_manifest(pack)
    particles = sorted((pack / "particles").glob("**/*.particle.json"))
    if not particles:
        fail(f"{pack}: no .particle.json files found under particles/")
    identifiers: set[str] = set()
    for particle in particles:
        validate_particle(particle, pack, identifiers)
    return particles


def package(pack: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(pack.rglob("*")):
            if source.is_file():
                archive.write(source, source.relative_to(pack).as_posix())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--output", type=Path, help="Write a .mcpack after validation")
    args = parser.parse_args()
    try:
        particles = validate(args.pack)
        if args.output:
            package(args.pack, args.output)
            print(f"Packaged {args.output}")
        print(f"Validated {len(particles)} Bedrock particle effect(s).")
    except ValueError as error:
        print(f"Bedrock validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
