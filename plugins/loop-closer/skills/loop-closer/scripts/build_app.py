#!/usr/bin/env python3
"""Build Neal's app version of Loop Closer (TTT fork).

Unlike build.py, no deck is baked in: the page reads today's tasks from the
artifact database, so one published page serves every day.

    python3 build_app.py --out loop-closer.html [--title "Loop Closer"]

Publish with capabilities {"db": {}, "sample": {"images": true}}.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "loop-closer.template.html"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="where to write the page")
    ap.add_argument("--title", default="Loop Closer")
    ap.add_argument("--tagline", default="Task Tinder, jacked")
    args = ap.parse_args()

    cfg = {"app": True, "title": args.title, "tagline": args.tagline}
    html = TEMPLATE.read_text(encoding="utf-8")
    if html.count("__CONFIG__") != 1:
        raise SystemExit("template must contain exactly one __CONFIG__ placeholder")
    html = html.replace("__CONFIG__", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    Path(args.out).write_text(html, encoding="utf-8")
    print("wrote %s (%d KB), app mode" % (args.out, len(html.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
