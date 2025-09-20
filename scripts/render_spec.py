import sys, os, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "dist" / "specbook.md"
parts = [
    ROOT / "spec" / "kit.yaml",
    *glob.glob(str(ROOT / "spec" / "requirements" / "*.md")),
    *glob.glob(str(ROOT / "spec" / "agents" / "*.md")),
    *glob.glob(str(ROOT / "spec" / "playbooks" / "*.md")),
]
parts = [Path(p) for p in parts if Path(p).exists()]
OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w", encoding="utf-8") as out:
    out.write("# Aura Analytics — Spec Book\n\n")
    for p in sorted(parts):
        out.write(f"\n\n---\n\n## {p.relative_to(ROOT)}\n\n")
        out.write(p.read_text(encoding="utf-8"))
print(f"Wrote {OUT}")
