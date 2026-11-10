"""Mechanical style checks from meta/DESIGN.md. Usage: uv run python tools/lint_pages.py [--summary]"""
import re
import sys
from pathlib import Path

SMALL = {"a", "an", "the", "and", "or", "but", "nor", "of", "in", "on", "to", "for", "with", "at", "by", "from", "as", "vs.", "into", "onto"}
REQUIRED = ["title", "author", "updated", "glance", "applies_to"]
NUMBERED_OK = set()
CERTIFIED = {"index", "contacts", "safety", "lab-spaces-and-dimensions", "computing-hardware", "admin-access-indoor-lab", "edit-the-wiki", "file-backup-server"}


def title_case_problems(text):
    words = re.findall(r"\.?[A-Za-z][A-Za-z0-9'\-./]*", re.sub(r"`[^`]*`|\[([^\]]*)\]\([^)]*\)", r"\1", text))
    bad = []
    for i, w in enumerate(words):
        if w.isupper() and len(w) > 1 or any(c.isdigit() for c in w):
            continue
        if w[0].isupper() or w[0].islower() and any(c.isupper() for c in w[1:]):
            if i > 0 and w.lower() in SMALL and (i == len(words) - 1 or words[i - 1] == '&'):
                continue
            if i > 0 and w.lower() in SMALL:
                bad.append(w)
            continue
        if i == 0 or w.lower() not in SMALL:
            bad.append(w)
    return bad


def check(path):
    out = []
    raw = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n", raw, re.S)
    body = raw[m.end():] if m else raw
    fm = m.group(1) if m else ""
    for k in REQUIRED:
        if not re.search(rf"^{k}:", fm, re.M):
            out.append(f"front matter missing {k}")
    if "assisted_by" not in fm:
        out.append("front matter missing assisted_by")
    body_nosnip = re.sub(r"```.*?```", "", body, flags=re.S)
    if re.search(r"^# ", body_nosnip, re.M):
        out.append("body has an H1")
    heads = re.findall(r"^(#{2,4}) (.+)$", body_nosnip, re.M)
    for lvl, h in heads:
        plain = h.strip()
        if plain.isupper() and " " in plain:
            out.append(f"ALL CAPS heading: {plain}")
        if re.match(r"\d+[\.\)]? ", plain) and path.stem not in NUMBERED_OK:
            out.append(f"numbered heading: {plain}")
        bad = title_case_problems(re.sub(r"^\d+[\.\)]?\s*", "", plain))
        if bad:
            out.append(f"Title Case: '{plain}' ({', '.join(bad)})")
    if len(heads) < 2 and len(body.split("\n")) > 40:
        out.append("long page with fewer than 2 headings (no TOC)")
    for lang, blk in re.findall(r"```(\w*)[^\n]*\n(.*?)```", body, re.S):
        if lang in ("python", "markdown", "md"):
            continue
        if any(l.lstrip().startswith("#") and not l.startswith("#!") for l in blk.split("\n")):
            out.append("code block has a comment")
            break
    if re.search(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", body):
        out.append("non-ISO date (MM/DD/YYYY)")
    if re.search(r"ask the admin", body, re.I):
        out.append("'ask the admin'")
    if re.search(r"^\s*\[[^\]]+\]\([^)]+\)\s*$", body_nosnip, re.M):
        out.append("standalone link not a button")
    for t in re.findall(r"^\|.*(?:Updated|Date).*\|\s*$", body, re.M):
        if "Last Updated" not in t and "Updated" in t:
            out.append(f"tracking table column should be 'Last Updated': {t[:60]}")
    for bad in ("Mocap Lab", "Outdoor Lab", "Husky A200 UGV", "Clearpath Jackal"):
        if bad in body:
            out.append(f"non-canonical name: {bad}")
    return out


def main():
    total = 0
    for p in sorted(Path("docs").rglob("*.md")):
        if "case-studies/example-parameters" in str(p):
            continue
        if p.stem in CERTIFIED:
            continue
        problems = check(p)
        if problems:
            total += len(problems)
            if "--summary" in sys.argv:
                print(f"{len(problems):3d}  {p}")
            else:
                print(p)
                for x in problems:
                    print("   -", x)
    print(f"{total} problems")


main()
