# Autonomy Park wiki: instructions for AI agents

Read these before changing anything:

- `meta/DESIGN.md`: the style guide and decision log. Follow it. In particular: code-block rules (section 8), no "ask the admin" (link the Contacts page), public-site safety (section 9), technical accuracy (section 10).
- `meta/TASKS.md`: the task board. Every change belongs to a task; update its status, commits, and "how to verify".

Hard rules:

- Work on a branch. Never commit to `main` (it auto-publishes). Small, single-purpose commits.
- Never invent commands, parameters, IP addresses, or safety guidance. If unsure, write "unknown" and add a question to `meta/TASKS.md`.
- The repo and site are public. No passwords, tokens, 2FA details, or personal data beyond what the maintainer approved.
- Never write security findings, or how credentials are arranged, into any tracked file. If `meta/private/` exists (local, gitignored), read it for open security items; keep such notes only there. Do not push or merge `overhaul/foundation` until Max has approved cleaning its history (see `meta/private/SECURITY.md`).
- Use `uv` (`uv sync`, `uv run mkdocs serve`). Build must show no `WARNING` lines.
- Large binaries go through Git LFS. Use `.jpg`, never `.jpeg`.
- Never infer a page's `author`. Ask Max; if he says unknown, write `Unknown` (rendered red italic). Same convention for any other missing fact (DESIGN section 6).
- Use the canonical names: Autonomy Park, Indoor Lab, SCC Lab. Never "Mocap Lab", "Outdoor Lab", or NCR (DESIGN section 3).
- Max Gardenswartz reviews and signs off every task.
