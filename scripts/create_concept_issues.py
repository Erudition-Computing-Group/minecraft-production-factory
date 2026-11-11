"""Create GitHub Issues for each particle effect concept from docs/particle-concepts.md."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

token = open("/mnt/c/Users/tpugh/.t3/userdata/secrets/files/711dcafa5aadc69a958d0da137adec25").read().strip()

from github import Github

gh = Github(token)
repo = gh.get_repo("Erudition-Computing-Group/minecraft-production-factory")

# Parse concepts from the markdown file
concepts_file = ROOT / "docs" / "particle-concepts.md"
content = concepts_file.read_text(encoding="utf-8")

# Extract numbered concepts
concepts = []
# Match lines like "1. **Name** — description" or "15. Name — description"
for match in re.finditer(r'^(\d+)\.\s+\*?\*?(.+?)\*?\*?\s*[—–-]\s*(.+)$', content, re.MULTILINE):
    num = match.group(1)
    name = match.group(2).strip().strip("*").strip()
    desc = match.group(3).strip()
    concepts.append((num, name, desc))

# Also match the "Additional cosmetic concepts" section (no bold, no em-dash variant)
for match in re.finditer(r'^(\d+)\.\s+(.+?)\s*[—–-]\s*(.+)$', content, re.MULTILINE):
    num = match.group(1)
    name = match.group(2).strip().strip("*").strip()
    desc = match.group(3).strip()
    if (num, name, desc) not in concepts:
        concepts.append((num, name, desc))

# Deduplicate by number
seen = set()
unique = []
for num, name, desc in concepts:
    if num not in seen:
        seen.add(num)
        unique.append((num, name, desc))
concepts = unique

print(f"Found {len(concepts)} concepts")

# Category mapping based on section headers
# Determine category by line position
categories = {}
current_cat = "Cosmetic"
for line in content.split("\n"):
    if "Layer 1" in line:
        current_cat = "Cosmetic"
    elif "Layer 2" in line:
        current_cat = "Ambient"
    elif "Layer 3" in line:
        current_cat = "Combat"
    elif "Additional cosmetic" in line:
        current_cat = "Cosmetic"
    m = re.match(r'^(\d+)\.', line)
    if m:
        categories[m.group(1)] = current_cat

# Edition mapping: first 14 are Java, rest could be either
# Based on docs, all are initially Java (Bedrock comes later)
edition_map = {}
for num, name, desc in concepts:
    edition_map[num] = "java"

# Math complexity from the taxonomy table
complexity_map = {
    "Galactic Rings aura": "High",
    "Cybernetic Glitch steps": "Low",
    "Phoenix Rise wings": "High",
    "Soul-Fire Halo crown": "Low/Mid",
    "Rainbow Ribbon trail": "Mid",
    "Cherry Blossom Breeze vortex": "Mid",
    "Cursed Void spasms": "High",
    "Deep-Sea Bubble vents": "Low/Mid",
    "Golden Treasure sparkle": "Low",
    "Soul Harvest kill effect": "High",
    "Critical Shockwave burst": "Mid",
    "Level Up helix": "Mid",
    "Enchantment Glyphs pull": "High",
    "Poison Cloud lingering": "Low",
}

created = 0
for num, name, desc in concepts:
    cat = categories.get(num, "Cosmetic")
    complexity = complexity_map.get(name, "Mid")
    
    title = f"[EFFECT] {name}"
    labels = [f"category:{cat.lower()}", f"complexity:{complexity.lower().replace('/', '-')}", "status:spec-ready"]
    
    body = f"""## Concept #{num}: {name}

**Category:** {cat}
**Math Complexity:** {complexity}
**Edition:** Java (Bedrock variant tracked separately)

## Visual Description
{desc}

## Motion Logic
See `docs/particle-concepts.md` for full motion logic and parametric equations.

## Tasks
- [ ] Concept & Spec: Create JSON spec (particle types, colors, budget)
- [ ] Math & Geometry: Solve and verify 3D formulas with Python
- [ ] Builder: Write Java/PaperMC emitter class
- [ ] QA: Compile, test TPS/MSPT, verify particle budget
- [ ] Visual Review: In-game check + record 10s preview GIF
- [ ] Storefront: Write listing copy + Tebex delivery command

## Acceptance Criteria
- Effect compiles and runs on PaperMC 1.21.4
- MSPT stays under 50ms with effect active
- Particle count stays under 150/tick
- Visual check approved by human operator
- 10s preview GIF recorded for storefront

## References
- docs/particle-concepts.md
- docs/particle-math.md
- docs/architecture.md
"""
    
    try:
        issue = repo.create_issue(title=title, body=body, labels=labels)
        print(f"Created #{issue.number}: {title}")
        created += 1
    except Exception as e:
        print(f"Error creating '{title}': {e}")

print(f"\nCreated {created} of {len(concepts)} issues.")
