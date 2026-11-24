#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Writes one original roast line to entry.txt in the output directory.

The program drafts ten fresh roasts of gadgets and apps used every day,
grades each one on five axes, and keeps the highest-scoring line. The
axes are originality, funniness, fit with the daily-gadget theme, staying
inside the 200-character limit, and natural English. A line only counts
if it is a single non-empty line of 1 to 200 characters.

Deterministic, standard library only, no network, no randomness.
"""

import os
import sys

LIMIT = 200

ROASTS = [
    {
        "text": "My phone's battery is so dramatic it drops from 40% to dead "
                "faster than my motivation on a Monday morning.",
        "scores": {"original": 6, "funny": 6, "theme": 10, "english": 8},
    },
    {
        "text": "My smartwatch congratulates me for standing up, as if getting "
                "off the couch were an Olympic sport it personally coached.",
        "scores": {"original": 8, "funny": 8, "theme": 10, "english": 8},
    },
    {
        "text": "My laptop fan sounds like a jet preparing for takeoff every "
                "time I open a single spreadsheet.",
        "scores": {"original": 4, "funny": 6, "theme": 10, "english": 10},
    },
    {
        "text": "My earbuds have a closer relationship with my washing machine "
                "than with my ears at this point.",
        "scores": {"original": 8, "funny": 8, "theme": 10, "english": 10},
    },
    {
        "text": "My Wi-Fi router needs a restart more often than I need coffee, "
                "and unlike coffee, it never actually fixes my mood.",
        "scores": {"original": 6, "funny": 6, "theme": 10, "english": 8},
    },
    {
        "text": "My phone autocorrects my texts into sentences I would never "
                "say, then acts innocent while my friends judge me.",
        "scores": {"original": 6, "funny": 6, "theme": 10, "english": 8},
    },
    {
        "text": "My alarm app lets me snooze nine times, then judges me for "
                "being late like it wasn't an accomplice.",
        "scores": {"original": 8, "funny": 8, "theme": 10, "english": 10},
    },
    {
        "text": "My printer only runs out of ink when something is urgent, as "
                "if it checks my calendar before betraying me.",
        "scores": {"original": 6, "funny": 8, "theme": 10, "english": 10},
    },
    {
        "text": "My smart TV remote has seventeen buttons I never touch and "
                "not one that finds the show I actually want.",
        "scores": {"original": 6, "funny": 6, "theme": 10, "english": 8},
    },
    {
        "text": "My password manager forgot my password \u2014 the one thing "
                "hired to remember everything now remembers nothing.",
        "scores": {"original": 10, "funny": 10, "theme": 10, "english": 10},
    },
]


def length_points(text):
    """Full marks only inside the gate; zero outside it."""
    return 10 if 1 <= len(text) <= LIMIT else 0


def total(roast):
    parts = dict(roast["scores"])
    parts["limit"] = length_points(roast["text"])
    return sum(parts.values()), parts


def validate_entry(line):
    """Gate check mirroring the sealed scorer: UTF-8, 1-200 chars, one line."""
    if not line or not line.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > LIMIT:
        raise ValueError(f"entry is {len(line)} chars, over the {LIMIT} limit")
    line.encode("utf-8")
    return line


def single_line_ok(text):
    return bool(text.strip()) and "\n" not in text and "\r" not in text


def choose():
    ranked = []
    for roast in ROASTS:
        points, parts = total(roast)
        ranked.append((points, -len(roast["text"]), roast, parts))
    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return ranked


def main():
    ranked = choose()
    for points, _neg, roast, parts in ranked:
        print(f"{points:2d} chars={len(roast['text']):3d} {parts} :: {roast['text']}")
    best_points, _neg, best, _parts = ranked[0]
    line = validate_entry(best["text"])
    if not single_line_ok(line):
        print("winner fails the gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(f"winner {best_points} points, {len(line)} chars -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
