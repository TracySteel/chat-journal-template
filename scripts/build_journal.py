#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
from datetime import datetime


def ts_to_iso(ts):
    try:
        return datetime.fromtimestamp(float(ts)).isoformat()
    except Exception:
        return None


def extract_messages(conv):
    mapping = conv.get("mapping", {})
    messages = []
    for node in mapping.values():
        msg = node.get("message") if isinstance(node, dict) else None
        if not msg:
            continue
        role = msg.get("author", {}).get("role")
        if role is None:
            continue
        content = msg.get("content", {})
        parts = content.get("parts") if isinstance(content, dict) else None
        if isinstance(parts, list):
            text = "
".join(str(p) for p in parts if p is not None)
        elif isinstance(content, str):
            text = content
        else:
            text = ""
        ts = msg.get("create_time") or msg.get("created_at") or msg.get("timestamp")
        try:
            ts_val = float(ts) if ts is not None else None
        except Exception:
            ts_val = None
        messages.append({
            "role": role,
            "text": text,
            "create_time": ts_val,
            "create_time_iso": ts_to_iso(ts_val) if ts_val is not None else None,
        })

    if any(m["create_time"] is not None for m in messages):
        messages.sort(key=lambda m: (m["create_time"] is None, m["create_time"] or 0))

    return messages


def build_search_blob(title, messages):
    parts = []
    if title:
        parts.append(title)
    for m in messages:
        parts.append(m.get("role") or "")
        parts.append(m.get("text") or "")
    blob = " ".join(parts)
    return " ".join(blob.split()).lower()


def main():
    ap = argparse.ArgumentParser(description="Build journal index + per-chat JSON files.")
    ap.add_argument("--input", required=True, help="Path to conversations.json (or sanitized)")
    ap.add_argument("--output", required=True, help="Output directory (e.g., site/data)")
    args = ap.parse_args()

    out_dir = Path(args.output)
    conv_dir = out_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    index = []

    for conv in data:
        if not isinstance(conv, dict):
            continue
        cid = conv.get("id")
        title = conv.get("title") or "Untitled"
        create_ts = conv.get("create_time")
        update_ts = conv.get("update_time")

        messages = extract_messages(conv)
        search = build_search_blob(title, messages)

        conv_out = {
            "id": cid,
            "title": title,
            "create_time": create_ts,
            "create_time_iso": ts_to_iso(create_ts),
            "update_time": update_ts,
            "update_time_iso": ts_to_iso(update_ts),
            "tags": [],
            "messages": messages,
        }

        if cid:
            out_path = conv_dir / f"{cid}.json"
        else:
            out_path = conv_dir / "unknown.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(conv_out, f, ensure_ascii=False)

        index.append({
            "id": cid,
            "title": title,
            "create_time": create_ts,
            "create_time_iso": ts_to_iso(create_ts),
            "update_time": update_ts,
            "update_time_iso": ts_to_iso(update_ts),
            "tags": [],
            "message_count": len(messages),
            "path": f"data/conversations/{cid}.json" if cid else "data/conversations/unknown.json",
            "search": search,
        })

    index.sort(key=lambda x: (x.get("create_time") is None, x.get("create_time") or 0))

    with open(out_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
