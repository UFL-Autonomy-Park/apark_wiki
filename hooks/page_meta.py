"""Draw the standard page header from front matter.

A page that has an `author` key gets, directly under its title:
  1. a byline box (author, updated, status, facility)
  2. an "At a glance" box built from the `glance` sentence(s)

Pages without `author` are left alone until they are migrated (meta/TASKS.md, T-006),
except that a `status` other than `active` always draws a status banner, with or without
an author, because a warning must not wait on authorship.
The contract for every key is in meta/DESIGN.md, section 6.
"""
import datetime
import html
import logging
import re

log = logging.getLogger("mkdocs.hooks.page_meta")

STATUSES = {"active", "deprecated", "unknown", "draft"}
FACILITIES = {"apark": "Autonomy Park", "indoor-lab": "Indoor Lab"}
UNKNOWN = "unknown"
STATUS_BANNERS = {
    "deprecated": ("Deprecated", "This page is kept for reference and is no longer updated."),
    "unknown": ("Status unknown", "Treat these instructions as unverified."),
    "draft": ("Draft", "These instructions have not been verified by an author."),
}


def _is_unknown(value):
    return isinstance(value, str) and value.strip().lower() == UNKNOWN


def _date(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value
    return None


def _as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _check(meta, src):
    for key in ("author", "updated"):
        if not meta.get(key):
            log.warning("%s: front matter is missing '%s'", src, key)
    for key in ("updated",):
        if meta.get(key) and not _date(meta[key]) and not _is_unknown(meta[key]):
            log.warning("%s: '%s' must be a date like 2026-10-21 (or Unknown)", src, key)
    if meta.get("status", "active") not in STATUSES:
        log.warning("%s: status must be one of %s", src, sorted(STATUSES))
    if "author_confidence" in meta:
        log.warning("%s: 'author_confidence' is obsolete; ask Max for the author, or write Unknown", src)
    for facility in _as_list(meta.get("applies_to")):
        if facility not in FACILITIES:
            log.warning("%s: applies_to '%s' is not one of %s", src, facility, sorted(FACILITIES))
    if "glance" in meta and not isinstance(meta["glance"], str):
        log.warning("%s: 'glance' must be one or two sentences (a string), not a list", src)


def _value(value):
    if value is None or _is_unknown(value):
        return '<em class="unknown">Unknown</em>'
    return html.escape(_date(value) or str(value))


def _byline(meta):
    esc = html.escape
    parts = []
    authors = ", ".join(_value(a) for a in _as_list(meta.get("author")))
    parts.append(f"<span><b>Written by</b> {authors}</span>")
    parts.append(f"<span><b>Updated</b> {_value(meta.get('updated'))}</span>")
    for facility in _as_list(meta.get("applies_to")):
        parts.append(f'<span class="page-meta__badge">{esc(FACILITIES.get(facility, str(facility)))}</span>')
    return '<div class="page-meta">' + "".join(parts) + "</div>"


def _banner(meta):
    status = meta.get("status", "active")
    if status not in STATUS_BANNERS:
        return ""
    title, default = STATUS_BANNERS[status]
    note = html.escape(str(meta.get("status_note") or default))
    return f'<div class="page-status page-status--{status}"><strong>{title}.</strong> {note}</div>'


def _glance(text):
    lines = ['!!! abstract "At a glance"', ""]
    lines.extend(f"    {line}".rstrip() for line in str(text).strip().splitlines())
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files):
    meta = page.meta
    banner = _banner(meta)
    if "author" not in meta and not banner:
        return markdown
    if "author" in meta:
        _check(meta, page.file.src_uri)
        header = _byline(meta)
        if isinstance(meta.get("glance"), str) and meta["glance"].strip():
            header += "\n\n" + _glance(meta["glance"])
        if banner:
            header = banner + "\n\n" + header
    else:
        header = banner
    fences = [m.span() for m in re.finditer(r"^(```|~~~).*?^\1", markdown, re.M | re.S)]
    heading = next(
        (m for m in re.finditer(r"^# .+$", markdown, re.M)
         if not any(a <= m.start() < b for a, b in fences)),
        None,
    )
    if heading:
        end = heading.end()
        return markdown[:end] + "\n\n" + header + "\n" + markdown[end:]
    title = meta.get("title") or page.title
    return f"# {title}\n\n{header}\n\n{markdown}"
