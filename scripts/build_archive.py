#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
import re

FM_RE = re.compile(r'^---
(.*?)
---
', re.DOTALL)


def parse_front_matter(text):
    m = FM_RE.match(text)
    meta = {"tags": []}
    if not m:
        return meta
    current_key = None
    for line in m.group(1).split('
'):
        if not line.strip():
            continue
        if line.startswith('- '):
            if current_key == 'tags':
                meta['tags'].append(line[2:].strip())
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip().strip('"')
            current_key = k
            if k == 'tags':
                continue
            meta[k] = v
    return meta


def main():
    ap = argparse.ArgumentParser(description="Build archive index and copy markdown files.")
    ap.add_argument("--input", required=True, help="Root folder containing markdown files")
    ap.add_argument("--output", required=True, help="Output folder (e.g., site/archive)")
    args = ap.parse_args()

    src = Path(args.input)
    out = Path(args.output)
    md_out = out / "md"
    data_out = out / "data"
    md_out.mkdir(parents=True, exist_ok=True)
    data_out.mkdir(parents=True, exist_ok=True)

    files = list(src.rglob('*.md'))
    index = []

    for p in files:
        rel = p.relative_to(src)
        dest = md_out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')

        text = p.read_text(encoding='utf-8')
        meta = parse_front_matter(text)

        entry = {
            "id": meta.get("id"),
            "slug": meta.get("slug"),
            "title": meta.get("title") or p.stem,
            "tags": meta.get("tags", []),
            "category": meta.get("category") or rel.parts[0],
            "file_path": meta.get("file_path") or rel.as_posix(),
            "md_path": f"md/{rel.as_posix()}"
        }
        index.append(entry)

    index.sort(key=lambda x: (x.get("category") or "", x.get("title") or ""))
    with open(data_out / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
