# Wiki Design Guide (draft v0.2, 2026-10-21)

Internal; not published. Edit freely. Anything marked **(proposed)** is waiting for Max.

## 1. Purpose and audience

The wiki is the **directory and companion** to the software stacks in
[github.com/UFL-Autonomy-Park](https://github.com/UFL-Autonomy-Park/). The repos say
*what the code does*; the wiki says *how to get the robot, network, and lab into a state where
the code works*, plus hard-won knowledge that would otherwise leave with a graduate student.

Design assumptions, in priority order:

1. **People do not read.** They arrive with a task, skim, and act. Put the thing that hurts
   them if missed at the top, short, and visually loud.
2. **Documented-but-unknown beats undocumented.** Pages may say "status unknown". Never leave a
   gap silent.
3. **Staleness is the main enemy.** Every page says who wrote it and when it was last true.
4. **The site is public.** No secrets, ever (see §9).

## 2. Information architecture (implemented 2026-10-21, under review)

Organize by what the reader is trying to do, not by who owns the hardware.

| Section | Contents |
|---|---|
| **Start Here** | Orientation: contacts, safety training, incident reports, rules, spaces, access (a sub-group), scheduling, FAQ |
| **Robots** | One hub per platform, all with the same sections (§5) |
| **Hardware** | Equipment that is not a robot: computers, Jetsons, controllers, RTK ground station, mocap, cameras, weather station |
| **Networking** | Network gear, reserving a static IP address, time sync, VPN, file backup server |
| **Software** | What we install and how: software list, IP reservations, flight practice, GitHub guide, virtual machines, simulation |

- Explicit `nav:` in `mkdocs.yml`, with top-level tabs. Folders mirror it: `start-here/` (with `access/`), `robots/`, `hardware/`, `networking/`, `software/`.
- Folder names: lowercase, hyphenated (`ground-robots`, not `Ground-Robots`).
- File names: lowercase, hyphenated, no spaces (`arm-motor assembly.md` is the known offender).

## 3. Two facilities, always say which

| | Autonomy Park | Indoor Lab |
|---|---|---|
| What | UF Energy Park field site (University resource) | MAE-A 313, motion-capture lab |
| Ownership | University | Dr. Kamalapurkar's lab; **not** a university resource |
| Network | Starlink LAN | Private LAN, not connected to the internet |
| Indoor flights | n/a | **Bebop only**, for safety |

Every page declares `applies_to: [apark]`, `[indoor-lab]`, or both, and renders a badge.
De jure lab in charge: **Systems, Controls and Cognition (SCC) Lab**, Dr. Rushikesh
Kamalapurkar. The Nonlinear Controls and Robotics (NCR) Lab / Dr. Dixon are no longer
affiliated and should not appear.

### Names (hard rule, decided 2026-10-21)

Pick one name per thing and never vary it, so a search finds everything and a newcomer never wonders whether two names are one place.

| Write | It means | Do not write |
|---|---|---|
| **Autonomy Park** (after the first mention, *the Park* is fine) | The outdoor field site at the UF Energy Park, a university resource | A Park, the outdoor lab, Outdoor Lab |
| **Indoor Lab** (first mention on a page: *the Indoor Lab (MAE-A 313)*) | The indoor motion-capture lab in MAE-A 313; belongs to Dr. Kamalapurkar's research group and is not a university resource | Mocap Lab, indoor mocap lab, the indoor lab (lowercase), the lab, MAE-A 313 alone |
| **SCC Lab** (first mention: *the Systems, Cognition, and Control (SCC) Lab*) | The research group (Dr. Kamalapurkar's) that runs both facilities | SCC's lab, our lab, the lab |
| **Husky A200** (title: Clearpath Husky A200) | The large Clearpath wheeled robot | Husky |
| **Jackal UGV** (title: Clearpath Jackal UGV) | The small Clearpath wheeled robot | Jackal |
| *(nothing)* | The former NCR Lab / Dr. Dixon's group | NCR, NCR Lab, Nonlinear Controls and Robotics. If a history sentence is ever truly needed, ask Max. |

Rules:
- *Indoor Lab* and *Autonomy Park* are places. *SCC Lab* is people. A page never says "the lab" by itself; it names the place or the group.
- **MAE-A 313** is a room number: use it for directions and room access, not as the name of the lab.
- Device hostnames such as `Husky706` or `Jackal570` are real identifiers and stay as they are. Where a literal name must stay because it is a real identifier (the `NCRLab` Wi-Fi SSID, a Drive document title), keep it **inside code formatting** and add *(legacy name)* the first time. Everything else gets the new name.
- Equipment keeps its own name (a computer called Steve is "Steve", not "the NCR computer").

## 4. Admonition ladder (proposed)

Use exactly these four. If unsure, go *down* a level.

| Type | Use when | Rule of thumb | Example |
|---|---|---|---|
| `danger` | Can injure a person or destroy expensive equipment | **Rare.** Max ~1 per page | Charging a swollen LiPo; arming with props on at a bench |
| `warning` | Will waste time or break the experiment if missed | Starts with the consequence | Skipping the DDS profile: nodes won't discover each other |
| `note` | Neutral context the reader may need | No urgency | Where a config file lives |
| `tip` | Optional shortcut | | A faster way to flash |

Style:
- Give every admonition a **short title** that states the point (`!!! warning "Props off for bench tests"`).
- **No ALL-CAPS paragraphs** in the body. The type already shouts.
- One idea per box. No lists longer than 3 items inside one.
- Do not use `note` for something dangerous because it "felt like a note".

Syntax:
```markdown
!!! danger "Never charge a swollen battery"
    Isolate it in the ammo can and tell a lab lead.
```

### Shared warnings (snippets)

A warning that appears on more than one page lives **once** in `snippets/` (repo root, not published) and every page includes it with a line such as `--8<-- "flight-modes-danger.md"` at the start of a line. Never copy-paste warning text between pages: copies drift, and a safety warning that differs between pages is dangerous. To change it, edit the snippet.

## 5. Page types and the "At a glance" box (proposed)

**Robot hub page** (one per platform). Order is fixed:

1. Byline (automatic)
2. **At a glance** box
3. Status banner if not `active` (deprecated / unknown)
4. Quick start (links to the SOP and the startup page)
5. Network and accounts (links, no secrets)
6. Known issues
7. Repos and further reading

**At a glance** is a 5-second answer to *"what is this, and why do I care?"*. It is **not** an overview or a summary of the page. It is one or two plain sentences, written in front matter as `glance:`, and drawn automatically as an `abstract` admonition directly under the byline.

- Start from the reader's stake: who is affected, and what is expected or at risk.
- No bullet lists, no links, no jargon the reader may not have yet.
- If it takes more than about 40 words, the page is trying to be two pages.
- Example (this wiki's edit guide): *"All users of the Autonomy Park and the Indoor Lab are expected to track their hardware issues, document useful facts, and correct errors in this wiki. This guide teaches how to edit it."*
- Prerequisites, repos and gotchas go in the page's own first section or in an admonition, not here.

The `abstract` admonition type is reserved for this box; do not use it elsewhere.

**Robot pages in the nav.** Every robot (or maker) has one nav group. Its pages come in this order, when they exist: **Overview** (picture, fleet, manual), **Set Up**, **Operate**, **Autonomy**, **Maintain**. A type with two or more pages gets its own nav sub-group and its own folder; a type with one page sits directly in the robot's group and folder. Makers with several robots (Freefly, Clearpath, Unitree) have a maker overview page first, and retired robots sit under a **Retired** group. Case study files drop the `case-study-` prefix, because their folder says it.

**How-to page**: goal sentence, prerequisites, numbered steps, "if it didn't work".
**SOP page**: purpose, who it applies to, hazards (as `danger`/`warning`), procedure, checklist.

## 6. Front matter (the byline contract)

Every page, no exceptions. Rendered by `hooks/page_meta.py`; the build warns on missing or invalid fields.

```yaml
---
title: Bebop Startup
author: Max Gardenswartz
updated: 2026-10-21
status: active
applies_to: [indoor-lab]
assisted_by: Claude
glance: >-
  One or two plain sentences: what this is and why the reader should care.
---
```

| Key | Required | Meaning |
|---|---|---|
| `title` | yes | Page title. The hook inserts the H1 from it if the page has none. |
| `author` | yes | Real name(s), comma-separated, **as told to Claude by Max**. If Max says the author is not known, write `Unknown`. |
| `updated` | yes | Last time the content changed (`YYYY-MM-DD`). |
| `status` | no | `active` (default), `deprecated`, `draft`, `unknown`. Anything but `active` shows a badge. |
| `applies_to` | no | `[apark]`, `[indoor-lab]`, or both. Omit for pages that are not facility-specific (such as editing the wiki). |
| `assisted_by` | no | `Claude` when an agent drafted or substantially edited the page. Kept as data only: the byline does not display it. |
| `glance` | on every robot, procedure and how-to page | One or two sentences (a string), see §5. |

Rules:
- **Never infer `author`.** Not from `git log`, not from file contents, not from the PDF metadata. Ask Max. If Max says unknown, the page says `Unknown`. Git history may be *offered* to Max as a hint, but he decides.
- `updated` may be taken from `git log` (it is a recorded fact, not a guess). If it truly cannot be established, write `Unknown`.
- Any edit that changes meaning bumps `updated`. There is no `verified` field: Max decided (2026-11-10) that the date updated is the only mechanism on the site.

### Unknown convention (everywhere, not only in the byline)

A missing fact is written as **<em class="unknown">Unknown</em>**, in red italics, never left blank and never guessed. It applies to authors, dates, versions, IPs, owners, statuses.

- In front matter: `author: Unknown`. The byline draws it red italic automatically.
- In page text: `*Unknown*{ .unknown }`. Example: `PX4 version: *Unknown*{ .unknown } as of 2026-10-21.`
- When a fact is unknown *and* someone could find it out, add the next step in plain words: *Unknown. Ask the people on the Contacts page.*
- Unknowns are a feature: they tell the next person what to fix. A page full of red *Unknown*s is more useful than a page that quietly guesses.

## 7. Media conventions (proposed)

**Images**
- Store in `docs/images/<topic>/`, lowercase-hyphenated names.
- Photos use the `.jpg` extension (never `.jpeg`) and are ≤ 1600 px on the long edge; `.jpg` is tracked in Git LFS regardless.
- Alt text is mandatory and describes *what to notice*, not "image".
- **All figures are formatted the same way (Max 2026-11-06, accepted my proposal).** Every figure has alt text. Widths: `60%` for screenshots, `50%` for photos of parts, `80%` for plan-view diagrams. A one-line italic caption is required for standalone figures (photos, maps, diagrams) and not used for step-by-step screenshots, where the step text is the caption. Checked in the final pass.
- Standard syntax: `![Alt text](../../images/homebrew/esc-finish.jpg){ width="60%" }`. Caption in the line below, in italics, when it teaches something.
- Screenshots of UIs: crop to the relevant window; **blur credentials, IPs, and personal names**.
- Do not use relative paths one level too shallow. Verify with `mkdocs serve`; CI runs a link check (planned).

**Video**
- Short clips (< 60 s, < 20 MB) can be stored in Git LFS as `.mp4`. Anything longer: upload to a UF-hosted/YouTube unlisted link and embed with a title and one-line description of what to watch for.
- Always give a text summary beneath a video; people skip videos.

**PDFs, and content that lives outside the wiki**
- **Lab-authored content is a page, never a PDF or a Drive file.** Pages are searchable, editable by anyone with the workflow, versioned, and show up in the nav. A PDF export of a Google Doc (the VM guide) is a snapshot that nobody updates.
- **Vendor manuals stay PDF** (we do not rewrite Unitree's manual). They live beside the page that cites them, are LFS-tracked, and the page links the PDF *and* says which section matters and what our lab does differently.
- A slide deck may stay a PDF download only if the page holds the full text too.
- Google Drive/Sheets links are a temporary state (T-015, T-037). Each one is tracked until its content is a page or a data table here.
- Link to other wiki pages with relative `.md` paths; never hard-code `https://autonomypark.org/...` (it breaks on any rename and cannot be checked by the build).

**Standalone links are buttons (Max 2026-10-21)**
- When a link is the point of a line (a map, a download, a form, a sign-up), make it a button: `[Label](url){ .md-button }`. Buttons are rounded site-wide (`extra.css`); never style one differently.
- Use a short label (what it opens, not "click here"). Links inside sentences stay ordinary links.
- Consecutive buttons sit on adjacent lines; the example is the map links on `start-here/access-requests.md`.

## 8. Lists, tables, code

**Tables that track things (Max 2026-10-21):** name the column **Last Updated** and put it **last**; write every date as ISO `YYYY-MM-DD` (`2025-08-21`), never `08/21/2025`. Other date columns (check-out, return) use the same format. Every such table follows this, so readers know where to look for staleness.

**Dates are ISO everywhere (Max 2026-11-06):** `YYYY-MM-DD` in every table, sentence and front matter, not only in tracking tables.

**Robot tables have a Ready to Fly column (Max 2026-11-10):** every table that lists individual robots has a **Ready to Fly** column (✅ / ❌, or *Unknown*). Ground robots use **Ready to Use** instead. Put it right after the robot's name, as on the Bebop Known Issues page. Do not guess the value: write *Unknown* until Max gives a rule or a value.

**Tables of equipment have a Last Updated column (Max 2026-11-03):** inventories and fleet tables (robots, batteries, computers, radios). Reference tables (parameters, status codes, pinouts, glossaries, settings) do not.

- Numbered lists only for ordered procedures; bullets otherwise. Keep bullets parallel in grammar.
- Tables for anything with ≥ 3 attributes per item (robots, batteries, IPs).
- Headings: sentence case; start at `##` (the title is the H1).
- **No numbers in headings (Max 2026-11-10).** Never write `1.0 Files` or `5.1 Binding`; the table of contents on the right is not numbered. Refer to a section by its name, with a link (`[Files](#files)`), never by "section 4.0". The lint rejects numbered headings.

### Code blocks (hard rules, Max 2026-10-21)

Every copyable block follows all of these:

1. **No comments inside a block (Max 2026-11-10: applies everywhere).** No `#` lines, no trailing `# explanation`, in command blocks and in blocks that show a file to copy (YAML, config). Explain in the sentence *before* the block. If a file's own comment lines matter, say so in a sentence. Shown program output is not a command: describe it in a sentence instead of pasting long output. `tools/lint_pages.py` checks every fenced block. (A `#` line inside a fence also used to break the page header; the hook now ignores fences.)
2. **One block does one thing.** Commands that always run together, with nothing to read, decide or edit in between, share a block. Test it as a lazy reader would: *paste the whole block and walk away; is the result what the sentence above promised?* Split a block when any of these is true:
    - the reader must look at output or make a choice between commands;
    - the commands run on different machines or in different terminals;
    - the commands have different purposes (switching a branch is not committing);
    - one command publishes or cannot be undone (`git push`): it gets its own block.
3. **No commands in running text.** Never write "run `git lfs pull`" or "check with `git lfs ls-files`" in a sentence. Put the command in its own block. Inline code is for file names, paths, identifiers, UI labels, and quoted output only.
4. **No prompt characters** (`$`, `>`) and no output mixed into a command block. Show output in a separate block labeled as output.
5. **Placeholders follow one of two conventions, never a third:**
    - **One-off value:** `<your-thing-here>`, explained in the sentence before the block.
    - **Value reused many times in a section:** set it once, in its own block at the start of the section, as an environment variable (for example `export HOMEBREW_NUMBER=05`). Every later command uses the variable (`$HOMEBREW_NUMBER`) and is therefore copy-paste modular. The sentence before the variable block says what to set it to and that it must be set again in every new terminal.
6. Always give the fence a language (`bash`, `powershell`, `yaml`).
7. **Say which operating system (Max 2026-11-10).** A page whose commands run on a lab computer says so once, near the top, in one sentence: "Everything on this page runs on a Linux computer." Say Linux, not a version; the Ubuntu version is on Software We Use. A page whose steps differ by OS uses tabs (Linux, Windows, macOS), and a page for a different OS (for example the OptiTrack machine on Windows) says that instead. Never leave the reader guessing whether a command is for Linux, Windows, or macOS.
8. **Say where the block runs.**
    - **One computer** (say, your laptop): state the computer and the working directory once at the top of the section ("Everything below runs on your laptop, inside the `apark_wiki` folder"), and again whenever either changes.
    - **Two or more computers** (for example SSH into a robot): **every** block carries a title naming the computer and, if it matters, the directory, in the form `title="Jetson · ~/ros2_ws"` (computer, a middle dot, directory). No block is allowed to leave the reader guessing which terminal it belongs in. Use the same computer names on every page (the names in the inventory, T-024).

Example of the split:

- Block 1: `git switch -c <branch-name>`
- Block 2: `git add` and `git commit` together
- Block 3: `git push`

## 9. Public-site safety rules

The repo and the site are public, and git history is permanent. Therefore:

1. **Never commit** passwords, tokens, Wi-Fi keys, router admin details, 2FA info, or shared-account credentials. State only *how to request access* and *who to ask* (link the Contacts page).
2. Treat internal IPs, device serials, room details, keycodes, and personal contact details as sensitive unless Max says otherwise.
3. Personal data (the roster) stays out of the repo until a publishing decision is made.
4. **Security findings and descriptions of how credentials are arranged are never written into any tracked file.** They go in chat, and if they need tracking, in `meta/private/` (gitignored, local only).
5. If a secret is committed by mistake: tell Max immediately; rotate the secret. Deleting the file does not remove it from history.

## 10. Technical accuracy

Robot instructions can break equipment or hurt people. Therefore:
- Content in areas Max does not own (Homebrew assembly, ground robots) is marked `status: draft` with a banner until an author verifies it. Placeholder is fine; confident-but-wrong is not.
- Claude never changes a command, a parameter value, a safety message's severity, or a step order without asking Max, and lists such changes explicitly in `TASKS.md`.
- Facts of record (confirmed by Max, 2026-10-21): only the Bebop flies indoors; the Homebrew is outdoor-only; the Go1 is the only robot safe in either place; RosBots are indoor-only; all Jetsons run JetPack 6.0 rev 2; lab computers run Ubuntu 22.04 with ROS 2 Humble (Python 3.10) and Gazebo Harmonic (latest available minor is fine; no minor version is known to break anything). Version constraints live in one place (TASKS T-030, to become the Compatibility page).

## 11. Tone

**Titles are Title Case (Max 2026-10-21).** Page titles, nav labels, and every heading use Title Case: capitalize every word except the short words *a, an, the, and, or, but, nor, of, in, on, to, for, with, at, by, from, as, vs., into, onto*, which stay lowercase unless first, last, or right after a colon. Everything else is capitalized, including *Is*, *Not*, *If*, and *Up* ("Do Not Set", "Back Up Your Parameters"). Words inside backticks, product spellings (`macOS`, `uXRCE`, `myMAE`), and acronyms keep their own form. Case-only changes do not break `#anchor` links.

**One heading theme everywhere (Max 2026-10-21).**
- Title Case only. No ALL CAPS: `1.0 Purpose`, not `1.0 PURPOSE`.
- Numbers (`1.0`, `1.1`) only on pages that people cite by number: PX4 Configuration and Flying Manually (the two SOP pages were removed on 2026-11-09). Every other page has no numbers.
- Tutorial steps are numbered list items, never headings: no `Step 1:` or `### 1. Do this` headings.
- No `# H1` in the page body: the theme shows the page title, and body headings start at `##`.
- The sweep is end-game work, with T-107 (table of contents), T-038, and T-040.


**Never write "ask the admin" (or "ask someone").** Name the people and link the [Contacts](../docs/start-here/contacts.md) page: the list of who to ask. If a person is not on that page, they are not the answer. Pages that depend on a person (e.g. a password holder) link to People too, so a staffing change is fixed in one place.

Second person, imperative, plain. Prefer "Do X" to "You should consider X". State consequences. Admit uncertainty: "Status unknown as of 2026-10-21; ask <role>."

## 12. Repository file conventions (proposed; the stricter rule set is TASKS T-042)

- Directories and files: lowercase, hyphen-separated, ASCII, no spaces, no underscores (`arm-motor-assembly.md`, `ground-robots/`).
- Extensions: `.jpg` (never `.jpeg`), `.png` for screenshots/diagrams, `.webp` for banners, `.md` for pages.
- **Folders and `.md` files are named after their titles on the website (Max 2026-10-21).** The name is the kebab-case of the page title or nav label (`Safety First` → `safety-first.md`, `Ground Robots` → `ground-robots/`). When you retitle a page, rename the file in the same commit. Existing files that do not match are renamed in the T-042 sweep.
- Directory tree mirrors the nav. A page lives in the folder named for its section.
- Images: `docs/images/<section>/<page-or-topic>/<descriptive-name>.jpg`, e.g. `images/homebrew/esc-soldering/good-joint.jpg`. Name by content, not by camera.
- A manual PDF sits next to the page that cites it, and is linked with a bare filename (`[Go1 Manual](go1-manual.pdf)`).
- Internal-only files live in `meta/`, never in `docs/`.
- **Files that are no longer used move to `unused/`** (repo root, outside `docs/`) with `git mv`, and are listed in `unused/README.md`. They are deleted together in one commit at the very end. Never delete them one at a time. Raw/unprocessed media lives outside the repo until chosen.
- Renaming a published page changes its URL. There are no redirects (Max 2026-11-06: we do not maintain compatibility with old links). The redirect hook and `redirects.yml` were removed.
- Dependencies: `uv` with `pyproject.toml` and `uv.lock`; no `requirements.txt`.
- Commits: on a branch, small and single-purpose, imperative subject with a `fix:`/`feat:`/`docs:`/`chore:`/`refactor:`/`build:`/`ci:` prefix.

## 13. Software installs: one hub, linked from everywhere (proposed)

- **Software Setup** (single page under Start Here) is the only place that says *how to install* a tool and *which version the lab uses* (uv, Git/LFS, ROS 2, Gazebo Harmonic, Docker, VPN client, QGroundControl, ...). One table at the top: tool, version, platform, where used. One short section per tool.
- Task pages carry a one-line **Requires:** (inside the "At a glance" box) linking to that section, and document only what is specific to *their* robot (e.g. a Bebop-specific DDS profile).
- Why: versions change; one page to update. Why not only the hub: people skim and land on task pages, so the *Requires* line must be on the page they land on.
- **Software We Use** (`start-here/software-setup/software.md`) lists every piece of software named anywhere in the wiki with the lab's version and where it is used. A page that introduces software adds a row (or checks that one exists); a final audit catches the rest.
- Tool-specific deviations ("the Jetson needs the ARM build") go in the hub section as a labelled sub-heading, not on scattered pages.

## 14. Operating-system tabs (hard rule, Max 2026-10-21)

Any step that differs by operating system uses content tabs, never separate headings and never a bullet that mentions another OS in passing.

- **Fixed labels and order, exactly:** `Linux / WSL`, `macOS`, `Windows`. The first tab is the one shown to a first-time visitor, so Linux is first on purpose (it is what the lab runs). Identical labels are what make the tab choice follow the reader from page to page (`content.tabs.link` is enabled).
- Steps that are the same everywhere stay **outside** the tabs. Only the differing step goes inside.
- Each tab follows the code-block rules (§8).
- If a task works on only one OS, say so in the "At a glance" box (`Runs on: Ubuntu 22.04 only`) and, where relevant, say why. Do not leave the other OSes silently missing. Robot-side work (Jetson, lab computers) is Ubuntu only and needs no tabs.
- Prefer a tool that works on all three OSes over three different procedures.
- Syntax:

````markdown
=== "Linux / WSL"

    Install the tool:

    ```bash
    sudo apt install <tool>
    ```

=== "macOS"

    Install the tool:

    ```bash
    brew install <tool>
    ```

=== "Windows"

    Install the tool:

    ```powershell
    winget install <tool>
    ```
````

## 15. Decision log

| Date | Decision | By |
|---|---|---|
| 2026-10-21 | All work on branches, small commits, Max reviews before merge to `main` | Max |
| 2026-10-21 | Move heavy files to Git LFS now; do not rewrite history | Max |
| 2026-10-21 | Byline = author, updated, status; Claude assistance documented | Max |
| 2026-10-21 | SCC Lab is lab de jure in charge; remove NCR/Dr. Dixon | Max |
| 2026-10-21 | Use `uv` + lock file, latest dependency versions where possible | Max |
| 2026-10-21 | `.jpg` only; no `.jpeg` | Max |
| 2026-10-21 | What the public site says about credentials: pending Max's decision (T-016) | Max |
| 2026-10-21 | IPs, SSIDs, router models, room numbers are OK to publish; passwords/2FA never | Max |
| 2026-10-21 | All titles and headings in Title Case | Max |
| 2026-10-21 | One heading theme: Title Case, numbers only on cited pages, steps as list items, no body H1 | Max |
| 2026-10-21 | Tracking tables: a last column named Last Updated, dates as YYYY-MM-DD | Max |
| 2026-10-21 | Call the robots Husky A200 and Jackal UGV everywhere | Max |
| 2026-10-21 | Folders and `.md` files are named after their website titles | Max |
| 2026-10-21 | Standalone links are rounded buttons (`{ .md-button }`), consistently | Max |
| 2026-10-21 | Personnel page: Max G., Opeyemi Owolabi, Dr. Kamalapurkar, with UF emails and photos | Max |
| 2026-10-21 | At project end, move unused assets to their own folder | Max |
| 2026-10-21 | Code-block rules (§8): no comments, one thing per block, no inline commands | Max |
| 2026-10-21 | "Ask the admin" is banned; link the Contacts page instead | Max |
| 2026-10-21 | Gazebo Harmonic, latest minor | Max |
| 2026-10-21 | Two-computer blocks get a `title="computer · directory"`; one-computer sections state it once (§8) | Max |
| 2026-10-21 | Placeholders: `<your-thing-here>` or an environment variable set at the start of the section (§8) | Max |
| 2026-10-21 | Never infer `author`; ask Max; unknown is written as red italic *Unknown* (§6) | Max |
| 2026-10-21 | At a glance = 5-second "what is this and why do I care?", 1-2 sentences, not an overview (§5) | Max |
| 2026-10-21 | Official lab name: Systems, Cognition, and Control (SCC) Lab | Max |
| 2026-10-21 | Names: Autonomy Park, Indoor Lab, SCC Lab; no Mocap Lab / Outdoor Lab / NCR (§3) | Claude, delegated by Max |
| 2026-10-21 | Software list built as we go, audited at the end (§13) | Max |
| 2026-10-21 | Unused files go to `unused/`, deleted in one final commit (§12) | Max |
| 2026-10-21 | Repeated warnings are shared snippets in `snippets/`, never copies (§4) | Claude, for Max |
| 2026-10-21 | OS-specific steps use `Linux / WSL` / `macOS` / `Windows` tabs everywhere, Linux first so it is the default (§14) | Max |
| 2026-10-22 | Homebrew **Case Studies** subsection: worked examples written from Max's notes, `Unknown` where the notes are silent; example parameter files only behind a danger box, never as templates | Max |
| 2026-10-22 | Pages are certified by Max in groups; a task that changes a certified page needs re-certification. Mechanical style checks run by script; the full style sweep runs once all content tasks are done | Max, Claude |
| 2026-11-03 | Cursed Knowledge page removed; its content lives with the Jetson flashing guide. Tables of equipment get a Last Updated column; reference tables do not | Max |
| 2026-11-06 | All figures are formatted the same way; the rule (captions or not) is still undecided, and the end-game sweep checks it (§7, T-134) | Max |
| 2026-11-06 | No redirects; old links are not maintained. The redirect hook was removed (§12) | Max |
| 2026-11-06 | Dates are ISO `YYYY-MM-DD` everywhere, not only in tracking tables (§8) | Max |
| 2026-11-06 | Page tags are the place tags (`applies_to`: Autonomy Park, Indoor Lab); every page has one, robot type tags are not needed (the nav already groups them) | Max |
| 2026-11-06 | The site never lists asset-tag or decal numbers, and never mentions them | Max |
| 2026-11-06 | No IP reservation tables anywhere; one IP Reservations page says where the lists are | Max |
| 2026-11-06 | No Infrastructure tab: Hardware, Networking, Software and Access tabs instead. Loaned Robots page removed. Every robot nav group follows Overview, Set Up, Operate, Autonomy, Maintain (§5). Files are named after their titles (kebab-case) | Max |
| 2026-11-09 | Safety and Access tabs removed: access pages are a sub-group of Start Here; the LiPo and Flying Quadcopters SOP pages are replaced by sections of Lab Rules; Report an Incident moved to Start Here; People renamed Contacts; Safety First renamed Safety; Lab Access Requests renamed Lab Access | Max |
