#!/usr/bin/env python3
import json
import argparse

ROLE_DROP_DEFAULT = {"system", "tool"}


def main():
    ap = argparse.ArgumentParser(description="Sanitize a ChatGPT conversations.json export.")
    ap.add_argument("--input", required=True, help="Path to conversations.json")
    ap.add_argument("--output", required=True, help="Output JSON file")
    ap.add_argument("--gizmo-id", default=None, help="Optional gizmo_id to filter (e.g., g-p-...) ")
    ap.add_argument("--drop-roles", default=",".join(ROLE_DROP_DEFAULT), help="Comma-separated roles to drop")
    args = ap.parse_args()

    drop_roles = {r.strip() for r in args.drop_roles.split(",") if r.strip()}

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    out = []
    for conv in data:
        if not isinstance(conv, dict):
            continue
        if args.gizmo_id and conv.get("gizmo_id") != args.gizmo_id:
            continue
        mapping = conv.get("mapping", {})
        for node in mapping.values():
            msg = node.get("message") if isinstance(node, dict) else None
            if not msg:
                continue
            role = msg.get("author", {}).get("role")
            if role in drop_roles:
                node["message"] = None
        out.append(conv)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
