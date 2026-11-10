# Task Board

Internal working document (not published; lives outside `docs/`). One entry per task.
Maintainer: Claude. Reviewer / sign-off: Max.

**Workflow.** Work happens on branch `overhaul/foundation`, in small commits. Every task
lists the commits that implement it and *how to verify it yourself*. Nothing reaches `main`
until Max has compared `uv run mkdocs serve` of the branch against the live site and signed off.

**Status key**

| Status | Meaning |
|---|---|
| `TODO` | Agreed, not started |
| `DOING` | In progress |
| `REVIEW` | Done on the branch, waiting for Max |
| `APPROVED` | Max signed off; ready to merge |
| `BLOCKED` | Needs information or a decision (see *Questions*) |
| `DECISION` | Max/PI must decide before work starts |
| `MAX-TBD` | Real-world action only Max can do (photos, checking a device, ...) |
| `AUTHOR-TBD` | Needs a subject-matter author; we leave a placeholder page |

**Review column.** Max: write `OK`, or a comment, in the *Max* line of the task.

**Setup for reviewing.** `git checkout overhaul/foundation && uv sync && uv run mkdocs serve`
(first time only: `git lfs install`).

## Lab-trip backlog (what needs a physical visit)

Strategy (Max 2026-10-21): get as far as possible without hardware, then stack up what needs a visit and do it in one trip per place.

| Where | Item | Task |
|---|---|---|
| *Nothing left* | Max cleared the backlog on 2026-11-10 | |

---

## A. Fixes (broken things)

### T-001 Remove the "ongoing work / to-do" lists — `APPROVED`
- Source: `docs/index.md` (Air Team, Ground Team lists). Out of date per Max.
- Commit: `0b49e21`.
- Verify: home page no longer has the section.
- Max:

### T-002 Images not rendering on autonomypark.org — `APPROVED`
- **Cause 1 (the invisible one):** `mkdocs-glightbox` 0.5.2 plus `selectolax` 1.x makes the plugin replace every content `<img>` with an empty `<p>`. glightbox 0.5.1 only worked because it pinned `selectolax==0.3.29`; 0.5.2 allows anything newer. **Fix:** keep glightbox latest, cap `selectolax<1` in `pyproject.toml` (documented there).
- **Cause 2:** 39 image links in pages under `quadcopters/{homebrew,freefly}/` used `../images/` (a nonexistent folder). Also a `.jpg.jpg` typo and `qx7_guide.jpg` vs `.png`.
- **Cause 3 (also in your `serve` log):** 11 broken links: PDFs linked via nonexistent `../../<dir>/` paths, a link to a nonexistent `parrot/` page, and `mymae.ufl.edu` with no `https://`.
- Commits: `ff9d97e` (image paths), `0a5a8e1` (uv + selectolax cap), `3673a87` (links).
- Verify: restart `uv run mkdocs serve`; logo and banners appear on the home page; Homebrew soldering pages show photos; terminal shows no `WARNING` lines (except the Material MkDocs-2.0 banner, which is upstream's notice and not about us). Full build: 134 of 134 images resolve.
- Note for later: Material says MkDocs 2.0 will break all plugins. We are on MkDocs 1.6.1 and the lock file keeps us there; revisit only if Material drops 1.x support.
- Max:

### T-003 Git LFS for heavy files — `APPROVED`
- Tracked: `pdf mp4 mov heic avif jpg` (see `.gitattributes`). 46 existing files converted (10 PDFs, 36 photos, ~110 MB).
- **History is not rewritten** (other editors active). New binaries are cheap from here on.
- CI fetches LFS with an object-hash cache (free LFS bandwidth is 1 GB/month; uncached CI would use ~110 MB per push).
- Commits: `b3701c9`, `4e2e100`, `9104b53`.
- LFS is documented in `contribute/edit-wiki.md` (T-018, `git log --grep='Edit the Wiki'`). Every editor must run `git lfs install` once.
- Risk to check after merge: first deploy must show real PDFs/photos, not pointer text. (CI only runs on `main`, so it cannot be tested from the branch unless we add a manual trigger.)
- Max: "I trust you."

### T-020 Dependencies via `uv` + lock file — `APPROVED`
- `pyproject.toml` + `uv.lock` + `.python-version` replace `requirements.txt`. CI uses `uv sync --locked`. Latest versions of everything; the only cap is `selectolax<1` (T-002).
- Removed the generated `src/apark_wiki/` package scaffold; this repo is a docs site, not an installable package.
- Commit: `0a5a8e1`.
- Max:

### T-021 File and folder naming convention — `APPROVED`
- Rule: DESIGN §12 (lowercase, hyphenated, ASCII; folders mirror the nav).
- Done in three commits (`git log --grep='refactor:'`): `.jpeg` → `.jpg`; 58 files moved into section folders with all 47 relative links rewritten by script (nothing hand-edited); 18 image files renamed (`Acc_wires.jpg` → `acc-wires.jpg`, `arm_assem/` → `arm-assembly/`). Build: no warnings; 338 of 338 file references resolve.
- **Old URLs are not kept (Max 2026-11-06):** the redirect hook and `redirects.yml` were removed. **Known gap:** direct links to moved *PDFs* (`/SOPs/quadcopter-sop.pdf`, `/tutorials/vmware-guide.pdf`, vendor manuals) are not redirected.
- Left as is, deliberately: `docs/images/` keeps its by-topic layout (not mirrored per section); `docs/apark.code-workspace` is still inside `docs/` and therefore **published on the site**. It looks like an accident; OK to move it out of `docs/` to the repo root (and change its folder path)? 
- `mkdocs.yml` still carries an odd `pymdownx.pathconverter` block (`base_path: "apark-wiki"`) that rewrites paths; it appears to be left over from an earlier deployment layout. I left it alone because removing it might change links; worth testing on its own.
- Max:

---

## B. Content and cleanup

### T-004 Asset register (used vs unused) — `DOING`
- Unreferenced in `docs/`: `images/gallery/20250425-park-visit.jpg`, `images/homebrew/solder-wick.jpg`. No unreferenced PDFs.
- **Used from `possible_assets/` so far (processed copies only, in `docs/images/`):** people photos (3, People page), `MAE-A 313.heic` (cropped, no people), `Autonomy Park Sky View.webp` (left panel only). The rest of `possible_assets/` (465 MB, untracked + gitignored) is not yet triaged.
- **Never publish without an OK:** photos with identifiable people (`Warren Dixon.jpg` and `UF NCR Logo.svg` are not to be used at all). Plan: table in `meta/ASSETS.md` (file, where used, people in photo, compress?, keep/drop).
- **End of project:** move unused assets to their own folder so the repo is lean (per Max). Folder chosen: `unused/` at the repo root (outside `docs/`, so not published). `unused/README.md` lists what is there and why: the old 1.16.0 `.px4`, three old parameter/script files, the group photo, and `solder-wick.jpg`. **One clean-up commit at the very end deletes the folder** (ask Max first). Rule: when a file stops being used, `git mv` it into `unused/`, never delete it one file at a time.
- Max:

### T-005 Remove Dr. Dixon / NCR Lab references — `APPROVED` (partial)
- Done (`git log --grep='NCR Lab from prose'`): 7 prose mentions in `procedures/quadcopters.md` (3), `bebop/bebop-startup.md`, `infrastructure/indoor-lab/indoor-lab-computers.md`, `infrastructure/computer-hardware.md`, `bebop/configure-network.md` (Wi-Fi password wording).
- **Deliberately left, because each names a real thing outside the wiki:**
    - SSID `NCRLab` and placeholder `$NCR_WIFI_PW` in `bebop/configure-network.md` → wait for T-027.
    - Drive document titles "Autonomy Park NCR Lab IP Reservations" / "IP Reservations - NCR Lab" (`configure-network.md` lines 38, 139) → `MAX-TBD`: rename the Drive files, then I update the text. These go away anyway when IPs move to the wiki (T-015).
    - `procedures/quadcopter-sop.pdf` title page names the NCR Lab → `MAX-TBD`: it is a controlled document; I need the editable source (Word/Docs) to revise it, and I will not edit the PDF.
- Judgement calls to check: `computer-hardware.md` now says only "Steve is located in NEB 405" (dropped "NCR office space"); `indoor-lab-computers.md` now reads "ALL USERS ON THE INDOOR LAB COMPUTERS". Severity of that box (`note`, all caps) is untouched; T-009 will propose a change for you to approve.
- **Also found in an image:** `images/freefly/fedex-shipping.png` (used by `repairs.md`) shows the former PI as supervisor and his overhead account as the funding source. The instructions it illustrates are out of date. `MAX-TBD`: a current screenshot with the right supervisor and funding source (blur anything personal), then I replace it and check the surrounding text.
- Max:

### T-006 Byline on every page — `APPROVED` (applied to 43 of 44 pages)
- Done (`git log --grep='bylines'`): authors applied **exactly** from Max's worksheet (`meta/AUTHORS.md`, answers pasted 2026-10-21); nothing inferred. `index.md` has no byline (Max). New pages this session (People, Software We Use, Parameters, Calibration Parameters, Upgrading PX4 Firmware, plus the earlier ones): author Max, assisted by Claude.
- **Rule from Max, applied:** any page I edit gets Max appended to the author list, `assisted_by: Claude`, and `updated: 2026-10-21`. **Judgment call to overrule if wrong:** 19 pages whose only change today was automatic link/path rewriting (folder move, image renames) were *not* counted as edited: they keep their original authors and last real edit date and have no Claude tag. Those pages: access-requests, videos, bebop/batteries, soldering, flash-jetson, radio-and-rc-setup, here4-firmware-upgrade, homebrew-docker, service-manual, ground-robot-startup, husky, jackal, procedures/batteries, asset-management, mocap-calibration, fileshare, zerotier-vpn, web-access, cursed-knowledge.
- `applies_to`: Homebrew pages are marked `apark` (outdoor only, per Max); the two Indoor Lab infrastructure pages `indoor-lab`; others unset.
- Still to do: `glance` sentences (T-010) and `verified` dates (only Max sets those).
- Max: sign off the look; overrule the 19-page call if you want them tagged.

### T-007 Design/style document — `APPROVED` (draft v0.2)
- `meta/DESIGN.md`. Expect revisions.

### T-013 Retired / working robots — `APPROVED` (partial)
- **Max 2026-11-10:** Okay as is (Max).
- **Alta-X:** retired, no batteries (Max). Done: `alta-x.md` has `status: deprecated` with a banner and the nav label reads "Alta-X (retired)". Page content is frozen.
- **Freefly Astro:** in working condition (Max). Done: Batteries section with Max's picture of the flight packs (flattened onto a light background; stored as `images/freefly/astro-flight-packs.jpg`); PX4 version recorded as red *Unknown*.
- **New feature:** a status banner (`status` + optional `status_note`) that appears with or without an author (`hooks/page_meta.py`). Replaces the badge in the byline box.
- **Please check:** the picture looks like a vendor render, not a photo of our packs; if it is Freefly's marketing image, we should confirm we may use it, or replace it with a photo from the shed. The caption says only what is visible (black packs, yellow label). I did not say what chemistry the packs are: the Astro page now has no battery-safety guidance, so please supply it or point me to the source.
- Astro fleet (Max 2026-10-21, now on `astro.md`): **three** Astros. astro1 software 2.3.7 and astro2 software 2.2.6, both PX4 base 1.15; astro3 *Unknown*. Controller (AMC) versions: astro1 latest from the Freefly Updater, astro2 second-latest, numbers `MAX-TBD` at the Park; astro3 *Unknown*. `astro_mavros` is being updated and tested with MAVROS 2.16.0.
- Still open for the Astro: astro3's versions; `repairs.md` (generic Freefly repair steps, also references the Drive); the all-caps warning block on `astro.md` (T-009). Authors for `astro.md`, `alta-x.md`, `repairs.md`: see `meta/AUTHORS.md`.
- Max:

### T-014 Homebrew parameter guide and case studies — `APPROVED` (part 1: PX4 Configuration)
- Done (`git log --grep='PX4 Configuration'`): `px4-configuration.md` reworked item by item from Max's review (listed in the commit message); new template `homebrew-px4-v1.16.2.params` replaces the inaccurate old one; comparison script rewritten as `px4-param-diff.py` (excludes only the calibration parameters; tested); `parameters.md` (from `homebrew_params.md`) and `calibration-parameters.md` (from `calibration_params.md`) added to the wiki and the nav; voltmeter picture added. Superseded files moved to `unused/homebrew/` (outside `docs/`).
- **Section 2.0 is verbatim** (Max: accurate). Section numbering kept (Max refers to sections by number).
- **Not yet verified by Max:** the contents of `parameters.md` and `calibration-parameters.md` (54 KB of tables). They are published as given. Sections still to review: every ✅/❌ row. Both pages have no byline yet (author?).
- **Answers received (Max 2026-10-21):** start with no props/battery and add the battery only when a step says (4.0 reworded); QGC menus differ between 5.0.x and 5.1.x (note added; screenshots will be 5.1.5); Quad X = `SYS_AUTOSTART` 4001 + `SYS_AUTOCONFIG` 1 and gives the quadcopter defaults the template sits on (explained on the page); the LiPo voltage checker is what the lab uses (no multimeter mention, it is more dangerous on a LiPo); a Requirements section lists QGC; the parameters must be read in the PX4 v1.16 reference only; torque-level control with RTK needs mainline PX4 and a parameter port.
- **ESC calibration, independently checked against PX4 v1.16 docs:** the doc says it applies to PWM/OneShot ESCs only (our template is PWM) and does **not** say where the calibration is stored or whether a firmware update or reset affects it. So Max's "once ever unless ESCs change; not stored in PX4" is consistent with PX4 but rests on Max's experience. Page says exactly that, plus the PWM/DShot context.
- Done after Max's next round: section 2.0 moved to `upgrading-firmware.md` (new page, nav entry); QGC labels checked against the v5.1.5 source (Q12): Tools > "Reset all to firmware's defaults", "Reset to vehicle's configuration defaults", "Reboot Vehicle", Q icon menu "Configure" are exact; WSL and Windows steps marked *Not verified*; Q15 accepted as is; Q18 answered (RTK facts, T-062); the "Missing parameters" message note added to the upgrade page.
- **Max 2026-10-21 (Q23):** upgrade verification and fleet roll-out rewritten on `upgrading-firmware.md` (good fix = `fix_type` 6, Position Mode drift, four steps for the fleet, skipping the wipe when calibration parameter names are unchanged). Skipping the wipe: if no calibration parameter names changed (including `BAT1_V_DIV`, `BAT1_A_PER_V`), battery recalibration is skipped too; load the revised `.params`, reboot, fly (Max). Other gaps in Q26.
- Case studies and observations (e.g. RTK obviates lidar and optical flow): `AUTHOR-TBD`, Max, later.
- Max:

### T-008 Navigation and information architecture — `APPROVED`
- Done: explicit `nav:` in `mkdocs.yml` with top-level tabs **Start Here · Robots · Procedures · Infrastructure · Contribute**; folders mirror it. DESIGN §2.
- **Judgement calls for you to check** (each is easy to move): People and Access Requests sit under *Start Here*; the Ubuntu/ROS install guide and setup videos are under *Start Here → Software Setup* (the future hub, T-028); *Asset Management* and *Computing Hardware* are under *Infrastructure*; the Indoor Lab pages (network, mocap) are under *Infrastructure → Indoor Lab*; *LiPo Battery Safety* and *Flying Quadcopters* (the SOPs) form *Procedures*.
- **Homebrew grouping (Build / Set Up / Operate) is my guess from page titles.** Order within each group is unverified. Max flies and configures these; he should reorder.
- There is no section yet for the RosBots, the Jetson inventory, or the compatibility page; they appear with T-022/T-024/T-026/T-030.
- Max:

### T-009 Standardize admonitions — `APPROVED` (titles Title Case everywhere except certified pages, 2026-11-06)
- Today: 11 note, 11 warning, 3 tip, 2 danger, inconsistent. Apply the ladder in DESIGN §4. **Technical care:** I will not change the *severity* of a safety message without asking you.

### T-010 "At a glance" box — `APPROVED` (drafted for all content pages, 2026-10-21; Max to approve or rewrite each)
- 2026-10-21: I drafted a `glance` sentence for the 42 pages that lacked one (not the home page, which has no byline, nor the empty ROSbot page). Pages I edited got Max appended to `author`, `assisted_by: Claude`, and `updated: 2026-10-21`, per the rule. Draft wording: read each page's box in `mkdocs serve`, then OK or rewrite. Pilot note follows.
- Now a 5-second "what is this and why do I care?", one or two sentences, in front matter (DESIGN §5). Pilot on `edit-wiki`, using Max's wording. For other pages I will draft the sentence and Max approves or rewrites.

### T-011 Introduce Autonomy Park vs. Indoor Lab — `TODO`
- Autonomy Park: UF resource. Indoor Lab (MAE-A 313, mocap): Dr. Kamalapurkar's lab, not a university resource. Landing page + `applies_to` badge on every page.

### T-012 Personnel and access — `TODO`
- Public page: **Max Gardenswartz, Opeyemi Owolabi (lab managers), Rushikesh Kamalapurkar (PI)**, with UF emails and photos. Emails are as given by Max. Photos are in `possible_assets/Misc/` (compress before adding; LFS).
- Document separately: (1) safety training complete, (2) Facilities has actually granted keycode access. Each lab (Autonomy Park, Indoor Lab) has individual keycodes.
- Trainee roster stays out of the repo until Max says otherwise.

### T-022 Robot environment matrix (indoor / outdoor / both) — `APPROVED`
- **Max 2026-11-10:** Done already (Max).
- **Statuses (Max, 2026-10-21):** Bebops: most still work, aging; Max tracks which work, which have problems, and the batteries in Google Drive (port later, T-015); the battery supply is dwindling, so they will eventually be replaced (e.g. Starling 2 Max). Huskies and Jackals: all work; one Husky has a battery that drains quickly (which one is *Unknown*), so both Huskies stay on chargers when not in use. B1: the single B1 is fully operational. Go1: all three are operational. Astros/Alta-X: see T-013.
- Earlier facts from Max: **Bebops** are good but aging; the biggest limitation is batteries (age unknown, they keep failing); the fleet is to be replaced soon, TBD, probably Starling 2 Max (T-049). **Astros:** three (see T-013). **Alta-X:** one, Gen 1, retired.
- A table in Start Here / Robots: each robot × {Indoor Lab, Autonomy Park}. Known: Bebop is the only quadcopter flown indoors (safety). Homebrew is outdoor only. Go1 is the only robot safe in either. RosBots live only in the Indoor Lab. Everything else: Max to confirm.

### T-023 Placeholder convention for unverified pages — `TODO`
- A standard banner (`status: draft` / `unverified`) for pages awaiting a subject-matter author, e.g. Homebrew assembly, ground robots. Max's rule: "unknown" is acceptable; undocumented is not.

---

## D. Infrastructure content

### T-015 Migrate IP reservations and equipment status from Google Drive — `APPROVED` (first batch done by T-093; Max 2026-10-21 unblocked it and said the wiki's Bebop battery and fleet tables replace the Google Sheets; the Batteries page no longer links the sheet)
- Needs Drive access. Max says IPs, SSIDs, router models, and room numbers are OK to publish (Q1). Still never: passwords or 2FA details.

### T-016 Credentials page — `TODO` (baseline agreed)
- What the public page may say about how access and credentials are handled is a security decision for Max. Details are intentionally **not** recorded in this tracked file (the repo is public); see the private notes Max has.
- **Agreed by Max (2026-10-21):** the public page says only *how to request access* and *who to ask* (link to the People page), and contains no passwords and no 2FA details. Where the detailed, access-controlled documentation lives: see T-047.
- Max:

### T-017 Security audit of the public repo — `APPROVED` (first pass done)
- Scope covered: all tracked text, all screenshots, and the full git history. **Findings were delivered to Max privately in chat and are kept in `meta/private/` (local, gitignored), not here, because this repo is public.** One item is urgent (action by Max in the real world).
- Public-safe follow-ups: the `fedex-shipping.png` form shows a former PI (added to T-005); `homebrew_params`/other pages: no action.
- New rule: security findings are never written into tracked files (DESIGN §9).
- Max:

### T-018 Editing guide: LFS, branches, `uv`, browser editing — `APPROVED` (part 1)
- Done: `contribute/edit-wiki.md` rewritten for git + git-lfs + uv, LFS section, branch/PR workflow, relative-path rules; tabbed per-OS install blocks (`pymdownx.tabbed`).
- Left: "Edit this page" button, GitHub PR template (*"Changed a robot? Update its page."*), front-matter/byline section once T-006 lands, style rules once DESIGN is signed off.
- Unverified by me: the Windows `winget` IDs and the Linux commands (written from the tools' documentation; I could only run macOS). Please sanity-check on a second OS when convenient.
- Max:

### T-019 Stale-page detection in CI — `DECISION`
- Warn when `verified:` is older than N months.

### T-028 Software setup hub page (ROS 2, Gazebo, uv, ...) — `DECISION`
- **Software list decision (Max asked, 2026-10-21): build it as we go, then audit at the end.** Done: `start-here/software-setup/software.md` ("Software We Use") exists as a draft with 18 rows from software already named on existing pages; versions not yet documented are red *Unknown*. Rule (DESIGN §13): any page that introduces software adds a row. At the end I run one pass that searches every page for software names missing from the table. Why as-we-go: it costs one row per page we touch and cannot become a big discovery job. Status: `REVIEW` (draft).
- Original proposal: ONE page, `Start Here → Software Setup`, is the canonical place for *how to install* each tool and *which version we use*. Other pages say "Requires: ROS 2 Jazzy (see Software Setup)" and only document what is specific to them. Details in the chat reply and DESIGN §13.
- Candidates already in the wiki: `start-here/software-setup/simulation-installation.md`, `contribute/edit-wiki.md` (uv/git/git-lfs), `vmware-guide.pdf`, `zerotier-vpn.md`.
- Max:

### T-030 Compatibility & upgrade constraints ("conventions") — `APPROVED`
Goal: one page (inside the Software Setup hub, T-028) that lists everything that restricts a version change, so anyone upgrading knows what they will break. Everything below is **as stated by Max on 2026-10-21 and not yet verified by me against vendor docs**; each row gets a source link and an "as of" date when written.

**Constraint chain (what dictates what):**

| Layer | Current | Set by / constrained by |
|---|---|---|
| OS (lab computers) | Ubuntu 22.04 | ROS 2 Humble target |
| ROS 2 | Humble | Driver support (below); dictates Gazebo version and Python 3.10 |
| Python | 3.10 | Ubuntu 22.04 / Humble default; limits the JAX version that runs on it |
| Gazebo | Gazebo Harmonic, latest minor (no minor version is known to break anything) | Ubuntu 22.04 / ROS 2 Humble recommend Harmonic |
| Jetson JetPack | 6.0 rev 2, all Jetsons | ZED SDK: it was the newest JetPack the ZED SDK supported as of Nov 2024 |
| ZED 2 cameras | `stereolabs/zed-ros2-wrapper` | Wrapper supports specific ROS 2 distros (Max: Humble, one more name garbled in message, Jazzy) and specific JetPack/CUDA versions |
| GPU code in Docker on Jetsons | CUDA from JetPack | Newer JAX needs newer CUDA, which needs newer JetPack |
| Ground robots (Clearpath Husky/Jackal) | vendor ROS 2 drivers | Clearpath supports specific ROS 2 distros and Ubuntu versions |
| NTRIP client (LORD/MicroStrain), Homebrew | in `homebrew_docker` | Check its supported ROS 2 / driver versions |
| ROSbots (to be documented) | old Ubuntu (e.g. 18.04) | Unknown whether the manufacturer publishes a ROS 2 driver that can be dockerized |
| Unitree Go1/B1, Bebop, PX4/Cube Orange | | Not yet listed; Max to add (PX4 firmware 1.15/1.16 files exist in repo) |

**Deliverables:**
1. A "Compatibility" table (component → supported versions → source link → as-of date → who verified).
2. An "Before you upgrade X" checklist per layer (e.g. *Upgrading JetPack: check ZED SDK + wrapper, CUDA vs JAX, Docker base image*).
3. A visible `warning` on pages that pin versions ("pinned because ...; do not change without reading Compatibility").
4. Later, link each row from the relevant robot's "At a glance" box.

**Needs from Max:** the garbled ROS 2 distro name, which Jetsons/ROSbots exist (T-024), and the `homebrew_docker` NTRIP version.
- Max:

### T-031 Code-block conventions sweep — `TODO`
- Apply DESIGN §8 (no comments, one thing per block, no inline commands) to every existing page. `contribute/edit-wiki.md` is done first (T-018). Likely worst offenders: `simulation-installation.md`, `radio-and-rc-setup.md`, `flash-jetson.md`, `configure-network.md`, `ros2-bebop.md`.
- **Technical-accuracy rule:** splitting/moving a command never changes it; commands with unclear intent get flagged to Max, not guessed.
- Max:

### T-032 Replace "ask the admin" with links to People — `APPROVED` (2026-11-06: done on `flash-jetson.md`, `ros2-bebop.md`, `web-access.md`; `fileshare.md` lines 57 and 71 still say "an admin" but the page is certified, so Max decides)
- Found: `edit-wiki.md` (3, done in T-018), `fileshare.md` lines 48 and 62 (password from "an admin"), `flash-jetson.md` line 70 ("Contact admin (Brandon as of 2025)"), `ros2-bebop.md` line 16 (NAS backups, "Reach out to the admin"). Several are about credentials: coordinate with T-016.
- Note: `flash-jetson.md` names a person who may no longer be here; Max to say who holds that password now.
- Max:

### T-033 Guide: adding collaborators to the Autonomy Park GitHub org — `APPROVED`
- Cover: organization **member** vs **outside collaborator** vs **repo-specific** access; teams; permission levels (read/triage/write/maintain/admin); who is allowed to invite (People page); when each is appropriate. Repo-specific collaborators should be **rare**; the guide says so and explains why (offboarding and audit are harder). Include removal/offboarding.
- Needs Max to confirm the org's current teams and default repo permission; I cannot see the org settings.
- Max:

### T-034 Should this repo have tests? — `DECISION` (discussion)
- My recommendation: yes, a few cheap automated checks, none of them "unit tests" in the software sense. Candidates, in priority order:
    1. **Strict build on every pull request** (`mkdocs build --strict`): catches broken links and missing files. Today CI only runs on `main`, i.e. *after* a mistake is live. This also lets us test the LFS-in-CI path from a branch.
    2. **Image/PDF reference check**: every referenced file exists, no unreferenced assets (T-004).
    3. **Front-matter check**: author, updated, status present on every page (after T-006).
    4. **LFS guard**: fail if a large binary is committed outside LFS.
    5. **Secret scan** (e.g. gitleaks): the repo is public (T-017).
    6. **Link check for external URLs**, run on a schedule rather than every PR (external sites flake).
    7. Optional: Markdown lint for the code-block rules (§8), spell check.
- Cost: a short workflow file and small scripts; maintenance is low if the checks stay simple. Risk: a noisy check that people learn to ignore, so each check must have zero false positives before it is required.
- Decision needed from Max: all of 1 to 5? Start with 1 only?
- Max:

### T-035 Guide: using an AI agent to update the wiki — `APPROVED`
- Human-facing page under Contribute: when an agent is appropriate, how to point it at the conventions (repo-root `CLAUDE.md`/`AGENTS.md` pointing at `meta/DESIGN.md`), the required habits (branch, small commits, `assisted_by` in front matter, human reviews every technical claim), what an agent must never do (invent commands, parameters, IPs, or safety guidance; commit secrets; push to `main`), and a short checklist for reviewing agent output. Includes the `uv`/LFS setup an agent needs.
- Max:

### T-036 Move the Ubuntu VM guide from PDF to its own page — `APPROVED`
- Source: `docs/start-here/software-setup/vmware-guide.pdf` (8 pages, a Google Docs export by Brandon Fallin, "Virtual Machine Installation Tutorial"). Becomes a normal page with screenshots as images (LFS), then the PDF is deleted so there is one copy.
- Fix the link in `start-here/software-setup/simulation-installation.md` line 8: it points to `https://autonomypark.org/ROS/vmware-guide.pdf`, which does not exist (the file is at `tutorials/`), so the link is dead today. Replace with a relative page link.
- Byline: author Brandon Fallin (from the PDF metadata); updated date unknown (`inferred`).
- **Accuracy:** I will transcribe, not rewrite, the steps. Max must verify the technical content (VMware, Ubuntu 22.04.5 ISO, disk sizes). Note the PDF may disagree with `simulation-installation.md` about disk space; I will list discrepancies for Max.
- Claude 2026-11-03: done. New page `start-here/software-setup/ubuntu-virtual-machine.md` (11 screenshots as LFS JPGs; the PDF is deleted; the dead link in Software We Use now points to the page; the VMware row links it). Transcribed, with these differences: (1) author is Brandon Fallin from the PDF metadata (Q59); (2) a student's Windows username in one screenshot is blanked out, and the example path is not copied; (3) "make the password easy to remember (like your UF login)" became "easy to remember", to avoid advising a UF password; (4) the Google Drive link to the VMware installer is not in the PDF, so the page links the vendor download on Software We Use; (5) the YouTube video (ROS 2 Jazzy install) is left out because its URL is not in the PDF. No disk-size conflict: the PDF's 20 GB matches Software We Use.
- Max:

### T-037 Audit: lab content living outside the wiki (the VM-guide logic, applied everywhere) — `DONE`
Rule (DESIGN §7): lab-authored content is a page; vendor manuals stay PDF; no hard-coded absolute site URLs. Findings from the first pass (2026-10-21):

| Where | Problem | Action |
|---|---|---|
| `start-here/software-setup/vmware-guide.pdf` | Lab-authored guide as PDF | T-036 |
| `procedures/quadcopter-sop.pdf` | A 16-page slide deck ("Quadcopters: Best Practices for Piloted and Autonomous Flight", dated June 15, 2026). The page `procedures/quadcopters.md` carries the text. | Decide: keep the deck as a download, but confirm the page has everything the deck has. Title page names the NCR Lab (T-029). |
| `procedures/quadcopters.md` lines 87, 93, 119 | Hard-coded `https://autonomypark.org/...` links; `/homebrew/diy-drone/` does not exist in the repo (dead); others are fine today but fragile | Replace with relative links; ask Max what the old diy-drone page was and where its parts list now lives |
| `bebop/batteries.md` | The Bebop battery tracking is a Google Sheet link | T-015 (migrate to a table) |
| `bebop/configure-network.md` (lines 38, 139) | IP reservations in a Google Sheet | T-015, T-029 |
| `freefly/astro.md` line 23, `freefly/repairs.md` lines 9, 11 | Pointers to a Drive doc, a Drive folder `Freefly Systems`, and a Sheet | T-015: pull the repair history and procedure into pages |
| Vendor PDFs (B1, Go1, harness, Alta X charger, Futaba T14SG, two Tattu, LW20 LiDAR) | Correct as PDFs; pages should say which sections matter | Part of the per-robot passes (T-009/T-010 era) |
| YouTube embeds (`ground-robot-startup`, `go1`, `b1`, `husky`, `videos`, `flash-jetson`, `access-requests`) | Content lives on YouTube; if a video is deleted the page silently breaks | Add a one-line text summary under each video (DESIGN §7); decide whether the lab owns/hosts the videos |
| `images/tutorials/*.png` screenshots | Possible secrets (T-017) | T-017 |

- Max: please add any other places you know of (e.g. Google Docs shared in Slack/email, the Chrome bookmarks in `web-access.md`).
- Max:

### T-038 OS tabs sweep — `LAST` (do at the end)
- Max 2026-10-21: do this last. Many pages are still to be written, and new pages follow DESIGN §14 from the start, so one sweep at the end is cheaper than repeated passes.
- Apply DESIGN §14 everywhere. First pass found:
    - `infrastructure/fileshare.md`: separate `Linux` / `Windows` / `macOS` headings, with mount commands and GUI steps → tabs. (Also uses `$PASSWORD`; see T-016.)
    - `infrastructure/zerotier-vpn.md`: `Windows and macOS` and `Linux` headings → tabs. The two share one tab only if the steps are truly identical; otherwise split.
    - `robots/quadcopters/homebrew/px4-configuration.md` line 38: a "Windows (PowerShell)" bullet inside running text, apparently with other OS alternatives → tabs.
    - `robots/quadcopters/homebrew/here4-firmware-upgrade.md`: Windows-only (Mission Planner); say so in the first lines, per §14.
    - `start-here/software-setup/simulation-installation.md`: Ubuntu 22.04.5 only; state it up front (it does) and link the VM guide (T-036) for Windows/macOS readers. macOS VM options (Apple silicon vs Intel) are unknown: Max to say.
    - `start-here/software-setup/videos.md`: VirtualBox install video: which host OS?
- **Technical accuracy:** I will only restructure existing commands into tabs. I will not write new macOS/Windows commands for robot workflows I cannot test; where an OS is missing, the tab says "not documented yet" and goes on the Max/author list.
- Also done already: `contribute/edit-wiki.md` (git, git-lfs, uv). `content.tabs.link` enabled in `mkdocs.yml`.
- Max:

### T-039 Lab Spaces and Dimensions: rename and add pictures — `APPROVED`
- **Max 2026-11-10:** Okay as is (Max).
- Done (`git log --grep='Lab Spaces'`): page renamed and restructured; typos fixed; per-axis table; Indoor Lab photo (cropped to exclude people), Park aerial (left panel of a composite), and a to-scale plan-view SVG of the Indoor Lab axes. **No number or direction was changed**; all values checked against the original text.
- **Please verify (I cannot):** (1) ~~the ceiling units are the mocap cameras~~ confirmed by Max; (2) the diagram's orientation: +x out the west window = left when north is up, +z north, as the original text states; (3) the SVG's label wording.
- Done at Max's request: the Spring 2026 expansion comment is removed. Not done: no photo of the Park's *inside*. Optional `MAX-TBD`: a current photo of each space with someone's OK, and a dimensioned sketch of the Park.
- `images/gallery/20250425-park-visit.jpg` stays unused: it shows identifiable people.
- Byline: author Max Gardenswartz (told by Max), `assisted_by: Claude`. Caption claim confirmed by Max: the ceiling units are the mocap cameras.
- Max:

### T-040 Terminology sweep: Autonomy Park / Indoor Lab / SCC Lab — `LAST`
- Max 2026-10-21: end-game. Content is not finished until the Google Drive and other outside material has been reviewed and moved in, so sweep once at the end.
- Apply DESIGN §3 "Names" to every page. First-pass counts (case-insensitive, `docs/`): "Indoor Lab" 13 variants (7 + 6 lowercase), `Outdoor Lab` 2 (both in the lab-spaces page), "the lab" or "our lab" 8, `SCC` 8, `NCR` ~12 (T-005 covers most; SSID/Drive titles stay as legacy names in code formatting), MAE-A 313 used as a place name in 2.
- Wording change only; no technical content changes. I list every changed sentence in the commit message.
- Max:

### T-041 Ask Max for each page's author — `MAX-TBD`
- Worksheet: **`meta/AUTHORS.md`**: one row per page (44), with a git-history *hint* and a blank column for Max. Max can edit it directly. I apply only filled rows and never blanks. Two rows are pre-filled (edit-wiki, lab-spaces).
- Applying the answers also adds the front matter, `updated` (last real edit from git, or today for new pages), and a draft `glance` sentence per page for Max to approve (T-006, T-010).
- Max:

### T-042 File naming: one convention for every file — `APPROVED` (done 2026-11-06: every file is named after its title) (sweep found 47 files whose name differs from the title; Max approved 2026-11-06 doing the renames together with T-146 so links change once; Max approved deleting `unused/` as the very last commit)
- **Max 2026-10-21 approved (now DESIGN §12):** folders and `.md` files are named after their titles on the website. Not yet done: the sweep that renames the existing mismatches (with redirects, link fixes, and `meta/AUTHORS.md` paths for Max to update). The rest (images, PDFs, versions, repeated folder names) is still for Max to decide.
Goal: the same rule for `.md`, images, PDFs, and data files, chosen for maximum readability. **Proposed rule (extends DESIGN §12):**
1. lowercase, ASCII, words separated by hyphens (`kebab-case`). No underscores, spaces, or capitals. Tool-mandated names (`README.md`, `CLAUDE.md`, `CNAME`, `pyproject.toml`) are exempt.
2. **A page's file name is the kebab-case of its short nav title**, so the name, the nav label, and the URL agree (`File Share` → `file-share.md`).
3. **Do not repeat the folder name** in the file name (`bebop/startup.md`, not `bebop/bebop-startup.md`); the path already says it.
4. Version numbers keep their dots and carry a `v`: `px4-v1.16.2`, not `1_16_2`.
5. Images: `images/<topic>/<what-it-shows>.jpg`, named for content, never the camera (`IMG_2041`).
6. A deck or companion file says what it is: `flying-quadcopters-slides.pdf`.

Current violations, with proposed names (each needs a redirect, which `redirects.yml` and `hooks/redirects.py` already provide):

| Current | Proposed | Why |
|---|---|---|
| `robots/quadcopters/bebop/bebop-startup.md` | `startup.md` | Rule 3 (nav title "Minimal Startup": maybe `minimal-startup.md`, Max to choose) |
| `robots/quadcopters/bebop/configure-network.md` | `wifi-setup.md` | Rule 2 (title says WiFi) |
| `robots/quadcopters/bebop/ros2-bebop.md` | `ros2-autonomy.md` | Rules 2, 3 |
| `robots/quadcopters/homebrew/homebrew-docker.md` | `docker.md` | Rule 3 |
| `robots/quadcopters/homebrew/homebrew-reference.md` | `quick-reference.md` | Rules 2, 3 |
| `robots/quadcopters/homebrew/how-to-fly.md` | `flying-manually.md` | Rule 2 |
| `robots/quadcopters/homebrew/compare_px4_params.py` | `compare-px4-params.py` | Rule 1 |
| `robots/quadcopters/homebrew/cubepilot_cubeorange_default_1_16_{0,2}.px4` | `cubepilot-cubeorange-default-v1.16.{0,2}.px4` | Rules 1, 4 |
| `robots/quadcopters/homebrew/homebrew_1_15_4.params`, `homebrew_1_16_2.params` | `px4-v1.15.4.params`, `px4-v1.16.2.params` | Rules 1, 3, 4. **Unverified:** I assume the numbers are PX4 versions; Max to confirm |
| `robots/ground-robots/ground-robot-startup.md` | `setup-videos.md` | Rules 2, 3 |
| `infrastructure/indoor-lab/indoor-lab-computers.md` | `network-setup.md` | Rules 2, 3 (title is "Indoor Lab Networking Setup") |
| `infrastructure/fileshare.md` | `file-share.md` | Rule 2 |
| `infrastructure/web-access.md` | `web-resources.md` | Rule 2 |
| `procedures/batteries.md` | `lipo-battery-safety.md` | Rule 2 |
| `procedures/quadcopters.md` | `flying-quadcopters.md` | Rule 2 |
| `procedures/quadcopter-sop.pdf` | `flying-quadcopters-slides.pdf` | Rule 6 (it is the slide deck) |
| `start-here/software-setup/simulation-installation.md` | `ros2-px4-setup.md` | Rule 2 (needs a shorter nav title too) |
| `start-here/software-setup/videos.md` | `setup-videos.md` | Rule 2 |

- Method: the same script as T-021 (moves the file, rewrites every link, and updates `redirects.yml` so old and older URLs both land on the new page). Build must stay at zero warnings.
- Risk: more URL churn. Redirects cover pages but not PDFs. Max: OK to proceed, and which of the "Max to choose" names?
- Max:

### T-043 Standardize attachment types — `DECISION` (later, per Max)
Proposal (to review when we get to it):
| Kind | Standard | Convert from |
|---|---|---|
| Photos | `.jpg`, ≤ 1600 px long side, in LFS | `.heic`, `.avif`, `.jpeg`, `.tif`, large `.webp` |
| Screenshots | `.png`, cropped to the relevant window | `.bmp`, `.gif` stills |
| Drawn diagrams | `.svg` where we can draw them; otherwise `.png` | |
| Video | `.mp4` (H.264/AAC), short clips only, in LFS; longer video hosted elsewhere with a text summary | `.mov`, `.avi`, `.mkv` |
| Manuals | `.pdf`, vendor-authored only; lab-authored content becomes a page | `.docx`, `.pptx` |
| Banners/logos | decide: keep `.webp` (2 files today) or move to `.jpg`/`.png` | |
- Currently in `docs/`: 41 jpg, 11 png, 10 pdf, 2 webp, 1 svg. `possible_assets/` has `.heic`, `.avif`, `.mov`, `.mp4` that will need converting before use.
- To decide: should `.png` go to LFS too (11 files, 2.7 MB today; screenshots can grow)? Add the standard to `tutorials`/edit-wiki once decided.
- Max:

### T-044 Document the mocap cameras: model and count — `APPROVED`
- Max to find out the camera model and how many the Indoor Lab has. Goes on the Indoor Lab pages and into the equipment inventory (T-024 style). Until then the page says *Unknown*.
- Max:

### T-045 Verify that cloning the repo works, following the Edit the Wiki page — `DOING`
- **Part A, done by Claude (2026-10-21):** fresh clone of the branch into an empty folder, then `uv sync --locked` and a full build. Result: clone OK; PDFs and photos arrive as real files (LFS smudge works); lockfile installs; build has no warnings; 51 LFS files.
- **Part B, `MAX-TBD` (needs the branch pushed, so it waits for the history cleanup, see T-017):** follow `contribute/edit-wiki.md` literally on a machine that has none of the tools, ideally one per OS (Linux/WSL, macOS, Windows). Record every place the page was wrong, missing a step, or confusing, and I fix the page. Specific risks: Windows `winget` IDs; SSH key setup is not covered by the page (the clone URL is SSH); whether new users get GitHub access in time; LFS bandwidth on first clone.
- **Part C, after merge:** confirm the first CI deploy publishes real PDFs/photos, not LFS pointer text (see T-003).
- Max:

### T-046 Roadmap: MAVROS to uXRCE-DDS, and torque-level control with RTK — `APPROVED`
- Done: a note in `start-here/software-setup/simulation-installation.md` and a warning on `px4-configuration.md`. Max's explanation (2026-10-21): **MAVROS does not support torque-level offboard commands; uXRCE-DDS does** but, in our current setup, forgoes RTK, which reaches PX4 over MAVLink/DroneCAN. PX4 PR #29368 (open, unmerged, no release as of 2026-10-21) would let ROS 2 send RTK corrections over uXRCE-DDS, which together enables torque-level control **with** RTK. The PX4 release containing it: *Unknown*.
- To do: move into the Compatibility page (T-030) as a "planned changes" entry; link from `homebrew-docker.md`; list what must be re-tested at the switch (MAVROS launch files, namespaces, the NTRIP/RTK path, `astro_mavros`, the parameter template, which currently configures MAVROS only). Update when #29368 merges. Q18.
- Max:

### T-047 Where robot credentials live — `DECISION`
- Robot logins are needed somewhere reliable and access-controlled (today's location is not good enough). Details are not recorded in this tracked file (public repo). The wiki lists only device name, username, IP, and a pointer to where to request access; it never lists the password. Revisit the credential columns on the Husky/Jackal pages with this task.
- Max:

### T-048 Clean old sensitive content out of the git history — `DEFERRED` (Max: not now)
- Old commits contain content that should not be public (details in the private notes). Real fix is rotating the affected secrets; a history rewrite (git filter-repo + force-push) is secondary. **Pre-condition for the first push:** the unpushed branch history must be cleaned or squash-merged. Max has confirmed he will not push until this is settled.
- Max:

### T-049 Starling 2 Max, and replacing the Bebop fleet — `APPROVED`
- **Max 2026-11-10:** Ignore; resolved.
- **Reminder to Max:** put the Starling 2 Max files in the wiki. A graduate student lent them to Max.
- Context: the Bebop fleet is to be replaced with new quadcopters (TBD, probably Starling 2 Max). Bebop limits: aging, and the batteries (age unknown) keep failing. When the decision is made: mark Bebop pages deprecated or "being replaced", add a Starling 2 Max hub page, and update the indoor-flight facts (today only the Bebop flies indoors).
- Max:

### T-050 Add a sky view of the Park to Access Requests — `DONE` (Max confirmed 2026-10-21; moved 2026-10-21 to Lab Spaces and Dimensions, Autonomy Park section, with the map buttons; Access Requests no longer has map links)
- Done: added as `images/facilities/autonomy-park-satellite.jpg` (LFS), below the map links, with alt text and a caption. **Please check:** the image looks like a map-provider screenshot (street names are visible); if it is Google imagery, the provider's attribution rules may require a credit. Not a people photo. Original (Max added it): `possible_assets/Misc/Autonomy Park on a Map.png` (1144 x 680). Goes on `start-here/access-requests.md` next to the existing map links (Max: the redundancy of map links is good, keep both). Process like the other photos (check for people, resize, LFS) and write alt text.
- Max:

### T-051 Document the Autonomy Park SITL and link it — `APPROVED`
- Document the Autonomy Park software-in-the-loop simulation and link the GitHub repo (UFL-Autonomy-Park org). Needs Max: repo name, how to run it, which PX4/ROS/Gazebo versions (ties to T-030). Probably belongs next to `simulation-installation.md`.
- Max:

### T-052 Which upgrades are safe and which need expertise — `APPROVED`
- Mark clearly, everywhere an upgrade is mentioned: **generally safe and non-breaking** (e.g. firmware on all our Emlid GPS units) versus **needs serious expertise** (e.g. changing the ROS 2 distro, updating PX4, JetPack). Probably a column in the Compatibility page (T-030) plus a standard admonition on the relevant pages. Needs Max's list of what is safe; I will not decide that.
- Max:

### T-053 Inventory the Emlid units — `APPROVED` (at the Autonomy Park **and** the Indoor Lab)
- **Max 2026-11-10:** Done already (Max).
- Max 2026-10-21: inventory all **rover** Emlids at both places. Max thinks all are RS models but maybe one RS2+. The ground station is an Emlid Reach RS3 (on `infrastructure/rtk.md`). Max to count how many Emlid GPS units the lab has (and ideally model and firmware). Goes in the equipment inventory (T-024) and T-052.
- Max:

### T-054 SOP summary of the most important safety rules — `DONE` (Max 2026-11-06: Lab Rules is the summary; no home page link; Safety pages link: Q64) (needs Max)
- A short, prominent summary (at-a-glance level) of the rules that matter most. Max's examples: eye protection; no quadcopters with batteries **and** propellers at the Autonomy Park outside the net. Draft from `procedures/quadcopters.md`, then Max edits; every rule is safety-critical and needs his sign-off. Link from the home page and robot pages.
- Max:

### T-055 PX4 Configuration needs pictures — `APPROVED`
- **Max 2026-11-10:** Covered by the Homebrew setup video (Max).
- Max to provide QGC screenshots (taken in the QGC version the guide targets; see Q11): Firmware tab flash, Parameters tools menu with the two reset options, the Reboot path, airframe selection, ESC wizard, voltage calibration, each sensor calibration, connection settings. Also confirms the exact menu labels (Q12). I will add alt text and the OS/version captions.
- Max:

### T-056 QGC configuration of the wireless radio — `APPROVED`
- Section 3.2 of `px4-configuration.md` now shows *Not yet documented*. Needs the radio model, QGC link settings, and a screenshot. (Max: Brandon or Max to write.)
- Max:

### T-057 QGC version warning everywhere QGC appears — `APPROVED`
- Done 2026-10-21: the Ubuntu 22.04 warning is now one shared snippet (`snippets/qgc-ubuntu-warning.md`) on `px4-configuration.md` and the QGC section of `simulation-installation.md`. The "written for 5.1.5" note stays only on the PX4 Configuration page. Still to do: the Compatibility page (T-030), and the preferred QGC build-from-source link (needs Max).
- Done on `px4-configuration.md`: QGC 5.1.x and later has no Ubuntu 22.04 binary and must be built from scratch; 5.0.8 is fine for the foreseeable future; the guide was written for QGC 5.1.5. To do: the same warning (or a pointer) on `simulation-installation.md` and in the Compatibility page (T-030). Link to the QGC build instructions once Max gives me the preferred source.
- Max:

### T-058 RTK: expect many errors until the fix resolves — `APPROVED` (needs Max)
- Document that with RTK, every quadcopter reports a lot of errors until the fix fully resolves, which takes 0 to 8 minutes (Max). Put on `how-to-fly.md`, `homebrew-docker.md` and the Homebrew pre-flight checklist. Needs Max: which errors, what a "fixed" state looks like in QGC, when it is safe to arm.
- Max:

### T-059 Mention that safety nets are a future safety feature of the Indoor Lab — `APPROVED`
- Done 2026-10-21 on `lab-spaces-and-dimensions.md` (Indoor Lab section), with when/where marked Unknown. The SOP summary (T-054) still to do.
- Add a short, dated statement that safety nets are planned as a future safety feature of the Indoor Lab: on `start-here/lab-spaces-and-dimensions.md` (Indoor Lab section) and in the SOP safety summary (T-054). The Autonomy Park already has its net (the rule about batteries and propellers outside the net is in T-054). Nothing says when or where the nets will go: *Unknown*, to be filled by Max. Do not imply they exist yet.
- Max:

### T-060 Homepage introduction — `DONE` (Max confirmed 2026-10-21)
- On the home page, say briefly what this wiki is, and what is meant by the **Indoor Lab** versus the **Autonomy Park**, including that only the Autonomy Park is a university-wide resource (the Indoor Lab is the PI's lab). Short; uses the canonical names (DESIGN §3). Drafted on `docs/index.md` (what the wiki is; a Park-versus-Indoor-Lab table with the "university-wide resource?" row; where to start). No byline (Max). Max: edit or approve the wording. Replaces the old to-do lists removed in T-001.
- Max:

### T-061 Fitting the Jetson snugly inside the Homebrew's shell — `APPROVED`
- **Max 2026-11-10:** Covered by the Homebrew setup video (Max).
- Document how to fit the Jetson snugly inside the Homebrew's shell. Max 2026-10-21 (problem): the shell that covers the Homebrew has no top space, so even with the Jetson pushed toward the center as far as possible, users still have to cut spaces for their cables and the Jetson still hits the top of the canopy. The 3 set screws holding the canopy do not seat perfectly, but they seat comfortably enough: they need only hand tightening and a little pressing on the canopy to "bend" it to fit. Max 2026-10-21 (Q28): he will take pictures to document this, at the Autonomy Park or the Indoor Lab (backlog). Still needed: the recommended fix (where to cut, which Jetson and carrier board). No page yet.
- Max:

### T-062 Document the RTK setup — `APPROVED` (draft page `infrastructure/rtk.md`; needs Max, see Q25)
- **Max 2026-11-10:** Already done (Max).
- Done 2026-10-21: draft page with the RS3 ground station (image, see Q25), RTKLib on the discovery server computer, never the embedded caster, the good-fix snippet, and the Emlid base station video (moved from Ground Robot Setup Videos, which now links here). Max 2026-10-21 (Q25): added the base location (main shed), setup, charging, equipment-cabinet note, and before-you-leave steps. Unknowns still on the page: Emlid Flow settings (T-074), RTKLib version and configuration, Indoor Lab, rover count (T-053). Max will send more RTK info later.
- Document: the settings on our ground station; how the drones connect; RTKLib; expected behaviour (including the errors until the fix resolves, 0 to 8 minutes, T-058); where corrections come from. Facts already recorded by Max and now on `px4-configuration.md`: QGC 5.1.5 RTK serving does not work (field-tested by Max) and nobody should serve RTK through QGC; the Autonomy Park uses a different setup for serving corrections; as of PX4 1.17.0 (so 1.16.2) the Micro XRCE-DDS Agent exposes no topic for RTK corrections, whereas MAVROS accepts them on `<mavros_namespace>/mavros/gps_rtk/send_rtcm`, published by an NTRIP client on a companion computer. Becomes a page under Infrastructure or Robots (to decide) and is linked from the Homebrew pages.
- Max:

### T-063 Downloadable attachments — `APPROVED`
- Done: the `.px4`, `.params` and `px4-param-diff.py` links on `px4-configuration.md` and `upgrading-firmware.md` now download instead of opening in the browser (`{ download="name" }`). To do: apply the same to other attachments that are meant to be saved (e.g. vendor manuals stay as normal links); add the pattern to the edit-wiki page.
- Max:

### T-064 Warn about flight modes: Stabilized needs expertise, Acro never — `APPROVED` (3 pages; SOP summary pending)
- Max 2026-10-21: flying in **Stabilized Mode requires expertise and must not be attempted by novice pilots**. **Acro Mode must never be attempted, under any circumstances.** **Position Mode is already quite fast: be very careful and move the sticks very slowly.** **Severity `danger`, approved by Max.** Done: one shared snippet (`snippets/flight-modes-danger.md`) included on `how-to-fly.md`, `procedures/quadcopters.md` and the Homebrew quick reference. To do: the SOP summary (T-054) and the Astro flying page (T-068) include the same snippet. The Position Mode caution is also on the upgrade page. **Q24 resolved by Max: do not arm in Stabilized; select Position (or the intended mode) before arming; once armed switching is very dangerous except Land or Hold. `how-to-fly.md` 4.1 and 4.2 corrected.** The SOP *page* now has the warning but the SOP *slide deck PDF* does not (T-037).
- Max:

### T-065 Warn about watching the battery while flying and while plugged in — `APPROVED` (shared snippet `snippets/battery-watch-danger.md` on how-to-fly, batteries, SOP page, quick reference; SOP summary T-054 and Astro page T-068 still to include it; severity `danger`, confirmed by Max 2026-10-21)
- Will be a shared snippet like T-064, so the Astro page and others include one text.
- Max 2026-10-21: although conservative failsafes have been added so that you cannot fly on a low battery, **the pilot must always watch the battery**. And **leaving a drone plugged in for long periods (e.g. 3 hours) does not prevent slow drain of the battery**: you can **easily** draw a LiPo below its safe limit (3.0 V per cell), which **permanently damages it with no warning at all from PX4**. Put on `how-to-fly.md`, `procedures/batteries.md`, `procedures/quadcopters.md`, the quick reference, and the SOP summary (T-054). Severity `danger` (Max confirmed).
- Max:

### T-066 Astro batteries are on firmware 2.1 — `APPROVED`
- Done: stated in the Batteries section of `astro.md`. Max: confirm the wording ("firmware 2.1" is the battery firmware, separate from the 2.3.7 / 2.2.6 software bundles).
- Max:

### T-067 Break up the Software Setup Videos page — `APPROVED`
- (Max 2026-10-21: the ground-robot videos page is already removed, T-102; only `videos.md` in Software Setup remains.)
- Max (author sheet): `videos.md` "will probably get broken up". Plan: each video moves to the page it illustrates (Ubuntu VM install with the VM guide, T-036; ROS 2 Humble install with the installation guide; Jetson flashing with `flash-jetson.md`), each with a text summary (DESIGN §7), then the page is removed with a redirect. Same for `ground-robot-startup.md` (videos for the ground robots). Needs Max: confirm the split, and who owns each video.
- Claude 2026-11-06: done. The VM video (`_T8p4ZprJkQ`) and the ROS 2 Humble video are embedded on `ubuntu-virtual-machine.md` (the Jetson video is already on `flash-jetson.md`); `videos.md` is removed with a redirect to the VM page and removed from the nav; the Software We Use rows no longer link it. The written guide is each video's text summary (DESIGN §7).
- Max:

### T-068 Flying the Astros — `APPROVED`
- **Max 2026-11-10:** covered by the Astro tutorial video on Flying Manually.
- A page on flying the Astros. Max expects to copy the flight warnings onto it: the flight-modes `danger` (T-064) and the battery warning (T-065) are shared snippets in `snippets/`, so it only needs an include line **once Max confirms each applies to the Astro** (which flight modes it has, what its battery management does, how the controller works). Do not copy the text by hand. Needs Max: the Astro flight procedure, controller (AMC) usage, failsafe settings (today a warning block of parameters on `astro.md`), and charging/storage.
- Max:

### T-024 Jetson inventory — `DOING` (page `infrastructure/jetsons.md` started; counting needs Max and helpers)
- All Jetsons run JetPack 6.0 rev 2 (per Max). Table: device, robot, JetPack, hostname, status. Needs Max to confirm per device.
- Max 2026-10-21: the lab has about 30 Jetsons. Most are set up, but they are not all labeled and no one has counted them. There are also Orin NXs that Max has not inventoried. Max suggests a page for the Jetsons, or an "Inventory" page (Q34). Max cannot reasonably do this alone and will ask others for help. First-pass data from the IP sheet (T-093): only about a dozen Jetsons have reserved IPs (Homebrew: 4, with homebrew-jetson-08 added 2026-10-21; Husky and Jackal: 4; Alta: 1; Unitree: 4), far fewer than 30. Counting and labeling the rest is a to-do for Max and helpers (backlog).

---

### T-069 Sweep standalone links into rounded buttons — `TODO`
- Max 2026-10-21 (design rule, DESIGN §7): a link that is the point of its line becomes `[Label](url){ .md-button }`, rounded site-wide. Done on the map links in `access-requests.md`. To do: sweep the other pages (downloads, forms, sign-ups). Do it near the end with T-038/T-040.
- Max:

### T-070 Qualify every mention of the Taranis QX7 — `APPROVED`
- Max 2026-10-21: the Taranis QX7 is Max's personal radio, not the lab's; he will not leave it when he graduates in 2028. Done: one shared note (`snippets/qx7-personal-note.md`) on `how-to-fly.md`, `parameters.md` and `calibration-parameters.md` (the three pages that mention it), linking to the radio page. Any new page that mentions the QX7 includes the same note.
- Max:

### T-071 Radio and RC page, with the NDAA-compliant recommendations — `APPROVED`
- **Max 2026-11-10:** the page is fine as is.
- Max 2026-10-21: the radio material in the Flying guide becomes its own page (today `radio-and-rc-setup.md`), including the recommendations in `NDAA Compliant RC Controllers.pdf` (Herelink Blue, Graupner mz-24 Pro, TBS Tango 2 Pro, ORQA FPV.CTRL, TX modules). Max has comments on those recommendations that should be documented. The PDF sits untracked in the repo root; it contains a person's phone number, so it is **not** committed. Needs Max: his comments and what to say about each controller.
- Max:

### T-072 Why `COM_ARM_HFLT_CHK` is off — `APPROVED`
- Done: reasoning in `parameters.md` now cites [PX4 issue #29346](https://github.com/PX4/PX4-Autopilot/issues/29346): a CubePilot Orange+ bug in PX4 1.16.2 where disconnecting USB hard-faults and leaves a log that blocks arming; easy to do by accident and harmless, so the check stays off until patched (likely PX4 1.19).
- Max:

### T-073 Verifying a good fix for quadcopters — `APPROVED`
- Max 2026-10-21: wherever a good fix is mentioned, say (1) `fix_type` in `<namespace>/mavros/gpsstatus/gps1/raw` is 6 always, and (2) that this has only been tested up to three quadcopters with RTKLib on the discovery server computer; the RS3's embedded caster is not reliable. Done as the shared snippet `snippets/good-fix-quadcopter.md` on `upgrading-firmware.md` and `infrastructure/rtk.md`. Max 2026-10-21: the Position Mode drift expectations are not part of the "good fix" text; they now live in `how-to-fly.md` section 4.4 (Homebrew-specific) and the upgrade page links there. To do: include it on the other Homebrew pages that discuss the fix (`how-to-fly.md`, `homebrew-docker.md`) with T-058.
- Max:

### T-080 Warn that the Here4 firmware update is for reference only — `APPROVED`
- Max 2026-10-21: add a `danger` to `here4-firmware-upgrade.md`: Max did this to compare RTK performance against the stock Here4 firmware (version unknown) on every Homebrew, found no difference, so it is for reference only and hopefully nobody has to use it. Done at the top of the page. **Check:** the page's intro still ends with "This tutorial may be relevant if the RTK setup you are using isn't working as expected", which now sits oddly next to the danger. I left it; tell me whether to remove it.
- Max:

### T-082 Rename Procedures to Safety, and mention safety in Start Here — `APPROVED`
- Done 2026-10-21 (Max: folder too; short page; remove safety stuff from Access Requests; loud reference): tab and folder renamed (`procedures/` to `safety/`, `git mv`); redirects for the old `procedures/` and `SOPs/` URLs updated (the SOP slide-deck PDF is not redirected); new `start-here/safety-first.md` holds the danger box, links to the Safety pages, and the video and quiz moved from Access Requests; Access Requests now opens with a danger box and a button to it. Old task text follows.
- Max 2026-10-21: change the **Procedures** top tab to **Safety**, and mention safety in the **Start Here** tab. To do on approval of Q30: rename the tab (and, to match DESIGN §12 "folders mirror nav", the `procedures/` folder to `safety/`, with `redirects.yml` entries, link fixes, and the references in `meta/` and `CLAUDE.md`); add the safety mention to Start Here.
- Max:

### T-098 Ask Brandon to update the B1 software portion — `AUTHOR-TBD` (Brandon Fallin)
- Max 2026-10-21: the B1 page's software section (SSH into the Jetson, the docker container, the ROS 2 startup script) needs Brandon to update it. Max to ask him. Together with T-097 (the Go1 ROS 2 startup).
- Max:

### T-112 Homebrew fleet page — `APPROVED`
- Max 2026-10-21 (with a pasted status list as of 2026-10-19): 21 Homebrews, numbered 02 to 22, no Homebrew 01 ("unnamed" is 22). Done: `homebrew/fleet.md` (lidar wiring, flight controller, crash history, notes, Last Updated 2026-10-19), a danger box about never powering on a wrongly wired lidar (shared snippet `snippets/lidar-wiring-danger.md`, also on the Quick Reference), Homebrew02's USB and slow XRCE (94 Hz) problem, and a note that the fleet needs to be indexed by Facilities. Interpretations to check (Q42): the list repeats 015 and uses leading zeros; I read them as 15, 17, 19, 11, 14, 16, 21; the "Bad FC" and crash lists are as given; Homebrews not listed as bad get "None reported". Not in the paste, so Unknown or omitted: whether each flown Homebrew is calibrated.
- Max:

### T-113 Indoor Lab IP reservations get their own page, so they cannot be confused with the Autonomy Park's — `APPROVED`
- Max 2026-10-21: move the Indoor Lab reservations to their own tab so they cannot be confused with the Autonomy Park reservations. My plan: two pages, `infrastructure/ip-reservations.md` (Autonomy Park only, renamed in the nav "Autonomy Park IP Reservations") and `infrastructure/indoor-lab/ip-reservations.md` (nav under Indoor Lab), each saying which network it is; links and redirects fixed. "Tab" is read as a separate nav page (Q42).
- Claude 2026-10-22: done as planned: `infrastructure/autonomy-park-ip-reservations.md` and `infrastructure/indoor-lab/ip-reservations.md`, each with a note saying which network it covers; links fixed; a stray header row and duplicate nav entries removed. Verify: open both from the nav.
- Max:

### T-117 Max's 2026-11-03 idea list: done now — `APPROVED`
- Claude 2026-11-03 (Max answered Q43 to Q55): **Astro** now says torque-level offboard control is impossible (Freefly, 2026-10-20), no SSH with app API v1 (stack uses v1; Freefly supports up to v4; AuterionOS v7), and the one-battery bench rule (danger box). **Fleet** has a "Flown by Max" column instead of "certified" (Max: certified lost its meaning after the lidar finding; Has Crashed and Flown by Max are the useful metrics). **Home page** has a Notices warning (multi-agent not possible now; needs RFD 900x radios and CBFs); this changes a page Max certified, so it needs re-certification. **Lab Rules** notes the Jackal loan predates the lending rule. **Schedule a Time** page (my suggestion: email a person on People) and the FAQ answer. **Who Has Access** lists the cleared people (Q58). **Autonomy Park frame** (origin, axes, shed) with `autonomy-park-axes.svg` on Lab Spaces and Dimensions (also a certified page; needs re-certification). **Security Cameras** (Lorex NVR). **Fixing an IP Address** (UniFi steps without login details, on purpose) and the Indoor Lab no-Internet note. **Building PX4** (CubePilot Orange, not Orange+, though the Homebrews have a Blue H7). The rule on Last Updated: only tables of equipment.
- Max:

### T-132 Come back to Who Has Access: a Canvas chain — `DROPPED` (Max 2026-11-06: the Who Has Access page is removed; the roster is private to lab managers)
- Max 2026-11-03: the cleared-only list is fine for now. Later he wants help setting up a chain with Canvas (if possible and free) so the list stays current. **Remind Max at the end of every session until done.**
- Max:

### T-131 Document all the networking equipment — `APPROVED` (Max, in person)
- Max 2026-11-03: it is all Ubiquiti; every switch, access point and so on needs to be documented in person. In the Lab-trip backlog.
- Max:

### T-118 Weather Station page — `APPROVED` (Max starts, Brandon finishes)
- Stub at `infrastructure/weather-station.md` using `UFL-Autonomy-Park/weather_package`. Needs: what the anemometer and barometer are, how to read both, where the data is (for reviewers who ask for local wind).
- Max:

### T-119 Guide: access the security cameras and pull footage — `APPROVED`
- Not started: no facts yet (see Q52).
- Max:

### T-120 Astro parameters reference — `TODO`
- Same treatment as the Homebrew parameters, simpler (the Astro stack 2.3.x is on PX4 1.15; Freefly does not port parameters on upgrade either). Needs a parameter export from an Astro (Max, in person).
- Max:

### T-121 Test Astro autonomy after the 2.1.x upgrade — `APPROVED` (Max, in person)
- **Max 2026-11-10:** Done: verified in a test flight on 2026-11-09; the new software works with astro_mavros.
- Unknown whether the new versions on astro1 and astro2 work with autonomy; needs validation. In the Lab-trip backlog.
- Max:

### T-123 Notice board on the home page — `APPROVED` (see Q50)
- Multi-agent experiments are not possible right now: more RFD 900x radios must be bought and CBFs do not exist yet. Max asked for a discussion first.
- Max:

### T-124 Slack join button, and where private repos are explained — `DROPPED`
- Max:

### T-125 Guide: fixing a Jetson's IP address — `APPROVED`
- The warning "set the IP before the hostname" is on the Jetson flashing guide. The steps are Unknown (see Q54).
- Max:

### T-126 Guide: building PX4 — `APPROVED`
- Max wants this to be how people make new (or get old) firmware for the Homebrews, instead of "download via QGC" (except for flashing the latest version). Then the wiki text that says to download from QGC (PX4 Configuration section 6.1, and T-077) must change. See Q54.
- Max:

### T-127 Every table gets a Last Updated column — `LAST` (final pass)
- Rule added to `meta/DESIGN.md` §8; the lint script gets a check once the exceptions are decided (see Q55).
- Max:

### T-128 How people schedule time at the Autonomy Park — `APPROVED` (see Q47)
- Max:

### T-129 Autonomy Park origin and frame, with a figure — `APPROVED` (see Q51)
- Max:

### T-130 Microhard radios page, when the first one is installed — `TODO` (future work)
- Max:

### T-133 Max writes the guide for updating ROS 2 — `APPROVED`
- **Max 2026-11-10:** Done: Software > Upgrading ROS 2.
- Max 2026-11-06: write a guide for updating ROS 2. It should cover: chrony setup at the Autonomy Park, RTKLib, `homebrew_docker`, and how many computers and robots must be verified for compatibility before an update can proceed. Links to the Compatibility page (T-030) and to T-046.
- Max:

### T-134 All figures formatted the same way — `LAST` (widths added to RTK, ZeroTier, PDB and arm-assembly images 2026-11-06; captions still to check)
- Max 2026-11-06: format all figures the same way; he is divided on whether captions are required. Added to `meta/DESIGN.md` §7. The final pass checks width, alt text and captions on every image.
- Max:

### T-135 Safety First: EHS trainings for the Indoor Lab only — `APPROVED`
- Max 2026-11-06 gave the content: EHS 809 (Hazardous Waste Management; all UF labs; once within the last 365 days, repeated) and EHS 869 (Chemical Hygiene Plan; the Indoor Lab has isopropyl alcohol and hot glue; once ever), with the MyTraining steps. Done: a section "EHS Trainings: Indoor Lab Only" on Safety First with a frequency table, the steps, and a button. Safety First is a certified page: needs re-certification.
- Max:

### T-136 Ubuntu VM: two pages, and Apple Silicon — `APPROVED`
- Max 2026-11-06: the video (by Wyatt Cross) is for VirtualBox; the written guide (by Keith Currier) is for VMware; clarify. Done: two pages, `ubuntu-in-vmware.md` (written steps; author Keith Currier, Max Gardenswartz) and `ubuntu-in-virtualbox.md` (the video; author Wyatt Cross; written steps Unknown); the ROS 2 video moved to Software We Use; both pages and Software We Use say Apple Silicon Macs are not covered (ARM-based Ubuntu; Gazebo GPU acceleration does not work; untested). Max decides whether to keep two pages.
- Max:

### T-137 Max 2026-11-06 answers (Q60 to Q69), applied — `APPROVED`
- Q60: figure rule accepted (T-134; to be written into DESIGN §7 and checked in the final pass). Q63: `start-here/software-setup/what-is-safe-to-upgrade.md` (T-052, T-030), with Planned Changes (T-046: the MAVROS to uXRCE-DDS switch is optional). Q65: the RTK fix waiting rule is in `snippets/good-fix-quadcopter.md`, now also on Flying Manually and Homebrew Docker (T-058). Q66: FAQ entry "How Do I Join the GitHub Organization?" replaces the long guide (T-033). Q67: nothing else outside the wiki (T-037). Q68: `contribute/using-an-ai-agent.md` (T-035; Max Gardenswartz, assisted by Claude). `upgrading-firmware.md` mentions PX4 PR 29363 (safe migration from 1.17 to the 1.18 beta) and that manual porting is the only safe way from 1.16. Redirects: none are added any more (DESIGN §12).
- Max:

### T-138 Max records a Jetson setup video — `APPROVED`
- **Max 2026-11-10:** Done: the setup video is embedded on the Homebrew Overview.
- Max 2026-11-06: a video on how to set up the Jetson, what to look for, and a general orientation to the RC and QGroundControl radio setups. It answers the Jetson-fit question (old Q28, T-061). A placeholder is on Homebrew Quick Reference ("Setup Video"); embed the YouTube link there when ready.
- Max:

### T-139 Software tab, Autonomy Park SITL page, Chrony Time Sync page, Lab Rules links — `APPROVED`
- Max 2026-11-06 (Q62, Q64, Q69, Q25, Q26b, Q28): **Software** is now a top-level tab (Software We Use, Ubuntu in VMware, Ubuntu in VirtualBox, What Is Safe to Upgrade, Autonomy Park SITL; the folder is `docs/software/`; all links fixed). **Autonomy Park SITL** is a short page (T-051). **Chrony Time Sync** (`infrastructure/chrony-time-sync.md`) is adapted from `homebrew_docker/docs/TIME_SYNC.md` with the commands unchanged (blocks split to one purpose each; the discovery server is `192.168.1.201` on the Autonomy Park network): check it against the original. Lab Rules link at the top of the two Safety pages. Planned Changes now has the `aero_common` and MicroStrain `ntrip_client` notes. T-077 dropped. Redirect entries that pointed to removed pages were deleted (they caused build warnings).
- Max:

### T-140 Everything about Slack and the email list (one task) — `DROPPED` (Max 2026-11-06: Slack is not mentioned anywhere on the site)
- Max 2026-11-06: do not worry about Slack for now; Max must ask Dr. Kamalapurkar his preference. There is an email list and a Slack that no one really uses. Merged here: the "join our Slack" button, the ufl.edu-email requirement for Slack, and where the invite goes (old T-124, Q49).
- Max:

### T-141 Max's 2026-11-06 answers (Q25, Q38 to Q42, Q49) and the LiPo SOP, applied — `APPROVED`
- **LiPo Battery Safety** now follows Max's slides: ammo cans (not crash-bins) in both places; three scenarios (dropped or damaged; retired: old, swollen, incorrectly charged; fire) with procedures; the full "Never" lists (battery handling, and in a fire); "lab manager" instead of "safety manager"; Title Case headings. **New page:** What to Do If There Is an Incident (equipment crash: tell Dr. Kamalapurkar; injury: medical attention, tell Dr. Kamalapurkar, EHS incident report, AmeriSys if University-employed); the Flying Quadcopters section 12.0 now points to it. **IP Reservations:** one page, no tables anywhere (the two IP tables and the Jetsons table are removed). **Homebrew Fleet:** the Facilities note is removed; a Sensors Calibrated column (Yes if Max flew it, plus Homebrew 10). **Lab Access Requests** (renamed) and **GitHub Access** (new, short). **Q25:** RTKLib access details live in `homebrew_docker` (not published); the Indoor Lab has no RTKLib; chrony is for the Indoor Lab in the future (Chrony Time Sync page). **Asset tags and decals:** the Loaned Robots asset-tag column is removed and the Freefly repairs page no longer names the sheet. Redirects: the hook and `redirects.yml` are removed (Max: old links are not maintained). Style guide: ISO dates everywhere, place tags only, no asset tags, no IP tables.
- Max 2026-11-06 follow-up (Q70 to Q74): the AmeriSys number is right; Fixing an IP Address now applies to both labs (both have UniFi; the gateway portal is `192.168.1.1` on each); the Bebop group and folder are now **Parrot Bebop 2** (`parrot-bebop-2/`); the Loaned Robots check-out date is 2026-07-08 and the return date 2027-01-01; IP Reservations has the two sheet buttons (IPs elsewhere stay); LiPo 8.1 says batteries stay in the ammo can until a lab manager orders a pickup and puts them in EHS 5-gallon bins; the ammo can locations are still Unknown (Q75). Max updates the ROSbot and Go1 `applies_to` himself.
- Max:

### T-142 Max 2026-11-06: Alta X name, no Who Has Access, ammo can location, no Slack — `APPROVED`
- "Alta-X" is now "Alta X" everywhere on the site and in the style guide. The Who Has Access page, its nav entry, its FAQ entry and `tools/roster_to_page.py` are deleted (the roster stays private). The Autonomy Park's ammo can is in the storage shed by the Venom chargers (LiPo SOP 2.2); the Indoor Lab's is still Unknown (to your to-do list). Stock photos stay as they are; the Bebop propeller-tool photos and the Go1 harness photo are not used. The site mentions Slack nowhere.
- Max:

### T-143 Max at the Autonomy Park 2026-11-06: results — `APPROVED` (later 2026-11-06: Emlid rover screenshots on RTK Setup; Networking Equipment has the IP column and is the Autonomy Park's; the Indoor Lab's equipment is on Max's to-do)
- **Astro:** AMC versions: astro1 `1.37.25-freefly-astro-2.1.0-gstreamer1.14`, astro2 `1.34.21`; astro3 stays Unknown (Max thinks it is in the Indoor Lab; not written down). New draft pages: Updating the AMC Version and Setting Up RTK on the Astros (three screenshots; username and password blurred; the password is in `homebrew_docker/.env.example`; no license is needed for third-party RTK); the Astro page has an "Updating and RTK" section (Freefly updates: see the Freefly docs). **Fleet facts:** two Huskies, both work, in the Park storage; three Go1s (Scooby at the Park; one in the Indoor Lab, name Unknown; one of Unknown location); three Jackals (jackal3 is in Panama City and must be recovered ASAP); one B1 in the Park storage shed; four Emlids labelled RS 001 to 004 and one RS3 (the ground station). **Networking Equipment** page from the UniFi list, with a how-to-read section. **Jetsons:** Mingyuan Gao counts and labels them; placement is covered by Max's video. **Bebop propeller tool:** two stock photos on Minimal Startup (Max rewrites that page). **Bathroom directions** are on the FAQ. All robot photos are stock; none are needed.
- Max:

### T-144 Recover jackal3 from Panama City — `MAX-TBD` (owner: Max thinks Wyatt Cross; not confirmed)
- Max 2026-11-06: jackal3 is in Panama City and needs to be recovered as soon as possible. Someone must be assigned to get it back.
- Max:

### T-145 RTK overview figure (editable) — `APPROVED`
- Max 2026-11-06: make a visual, not generated, that Max can edit later, explaining RTK: ground robots use LoRa from the RS3; quadcopters use local NTRIP and a caster (RTKLib on the discovery server). Done: `docs/images/facilities/rtk-overview.svg`, hand-written SVG (open it in a text editor or Inkscape; the clipart dog is embedded as a data URI in the one `<image>` tag, so it can be swapped), drawn from Max's whiteboard sketch (`Sample RTK Setup Overview.jpg`) and `Robot Dog Clipart.jpg`. On RTK Setup under "How Corrections Reach the Robots". Check it: Q79. 2026-11-06 later: Max approved the figure; the main shed box now lines up with the storage shed box, and the quadcopter motors are no longer cut off. Also 2026-11-06: all four rover Emlids are RS+ and identically configured; two better Astro USB-C photos replaced the old one (dust cover, and port).
- Max:

### T-147 Home and Start Here overhaul (Max's notes, 2026-11-09) — `APPROVED`
- Max 2026-11-09 (notes on Home and Start Here). Done: homepage cut to a tagline, a Start Here banner, a notice, and five cards; Safety First renamed Safety; Safety tab removed (LiPo and Flying Quadcopters pages and `quadcopter-sop.pdf` deleted; their key rules are now sections of Lab Rules: Flying, LiPo Batteries); new rules (no flying in weather, never enter the net while a quadcopter is armed, read a robot's documentation before use); Report an Incident moved to Start Here and linked from Lab Rules; FAQ moved last, draft banner removed, questions added (including passwords); Lab Access Requests renamed Lab Access with form data as tables; Requesting Admin Access renamed Admin Access (Indoor Lab) with the two-week wait; "People" renamed "Contacts" everywhere; Start Here overview page drafted (status draft, waits for Max's approval); Access is a sub-group of Start Here between Lab Spaces and Dimensions and Schedule a Time; both plan-view figures lost their embedded captions; the Autonomy Park figure has both sheds on the -y edge, storage shed 4x3 (long side along x), main shed 3x4 (long side along y); Miscellaneous Equipment page added in Hardware (walkie-talkies, shed contents). Report an Incident sits before Lab Rules in the nav.
- **Open:** walkie-talkie details; what the weather rule should say about wind or temperature limits (it says only "rain, storms, or other bad weather"); an inventory of the Indoor Lab computers (Max returns to this, see T-085); the Start Here overview needs Max's approval.
- Max:

### T-148 Max's notes on Bebop, Freefly, and Astro pages (2026-11-09) — `APPROVED`
- Done: Home buttons centered and Robots card linked; Admin Access steps as a table; Bebop pages (Overview, Known Issues with colored circles and a Ready to Fly column, Batteries, Connecting to WiFi [danger box], Setup, Autonomy stub, Firmware Update trimmed to the firmware steps with the Drive link); Known Issues pages for Bebop, Homebrew, Astro; Sending Drones for Repair rewritten (screenshot removed, tables, foam admonition); Astro Overview, RTK Setup (table, no Steps), MAVROS (verified, table), Parameters (Max's list; TC_* on one line); RTK intro on both RTK pages; robot names dropped from page titles (Astro, Homebrew, Husky, Unitree).
- Max 2026-11-09 (second batch): Dixon was in the screenshot. Repairs (renamed from Sending Drones for Repair) now has the myMAE request as a field table, copied from the old screenshot, with Dixon replaced by Rushikesh Kamalapurkar (supervisor and funding source). Bebop Batteries has the dispose-of-old-batteries notice; Bebop Setup is a numbered list with a Next link; Bebop Autonomy has a place for the YouTube video (commented out). B1 and Go1 ask for Brandon Fallin's help. Overview pages for Clearpath, Unitree, Freefly, and Homebrew (the old Quick Reference); Fleet and Known Issues are now direct Homebrew pages. Soldering Tutorial moved to Hardware and is linked from Motor Soldering Guide. New Overview pages under Homebrew Build (draft, asks Mingyuan Gao) and Set Up. Jetsons cleaned up with a note that there are no JAX wheels. Radio and RC Setup Guide uses standard admonitions. Go1 and B1 product images have a white background instead of black.
- **Open:** the Harness page never had a product image (none in the repo or its history); Max offered to supply one. The myMAE "Shipping Label Pick Up Options" value is Unknown. The funding source was "Dr. Dixon's overhead account"; it now says Dr. Kamalapurkar's, which may not be the right account.
- Max:

### T-152 Max's third batch (2026-11-10): Astro, Homebrew, Bebop, style guide — `APPROVED`
- Done: Harness image (first page of `harness-manual.pdf`, `unitree-harness.jpg`); Emlid Flow App Store and Google Play buttons and the "Single" note on RTK Setup; the SD-card slow note moved from Homebrew Overview to Known Issues (Parameters links to it; `sd-card-danger.md` removed); Astro: Status Codes, Updating the AMC Version and Homebrew Fleet pages deleted, MAVROS renamed Autonomy, Flying Manually (draft) added, never-update-Herelink danger box, `https://10.41.1.1/` over USB-C on USB-C Port and Dashboard, three ways to change parameters; Homebrew RTK Setup (draft); Homebrew Known Issues has PX4 (1.16.2, 1.18beta for 14) and Ready to Fly columns; Ready to Fly or Ready to Use column on the Astro, Go1 and Jackal tables (all *Unknown*); style guide: Ready to Fly column, no comments in any block, state the OS; Bebop Firmware byline: the page had no header because a `#` line in a code block was taken for the H1; the hook ignores fences now; comments removed from the Bebop Firmware and Indoor Lab Networking code blocks.
- Fleet's Flight History table was deleted with the page (it is in git history: `git show HEAD~:docs/robots/quadcopters/homebrew/fleet.md` before the deletion commit).
- **Open:** Q84 to Q87.
- Max:

### T-160 Max's tenth batch (2026-11-10): Indoor Lab facts, Astro readiness, config files — `APPROVED`
- Max 2026-11-10: T-044 (20 OptiTrack Prime 17W mounted; spares' location unknown), T-027 (`NCRLab` and `NCRLab_5GHz`), T-142 (Indoor Lab ammo can on a bottom shelf), T-131 (USW Lite 19 PoE, U7 Pro, Cloud Gateway Ultra; the UniFi list is still missing), T-150 (`main.cal` is the Indoor Lab calibration; it is already on the Motive computer in `C:\Motive 2.02 NCR Calibration Files`; new spaces need new calibrations), T-094 (three netplan files). T-118 and T-056 done by Max. Q86 (astro1 ready; astro2 flies but its remote has range issues; astro3 in storage), Q89 (5 MB/s; names checked against the v1.16.2 source: `MC_AIRMODE`, `MC_BAT_SCALE_EN`, `MPC_THR_HOVER` and `SDLOG_PROFILE` are real, `BAT_SCALE_EN` and `MC_AIRMODE_EN` are not), Q90 (assigned to Brandon, in the note on Go1).
- Config files in `docs/networking/configs/`, copied byte for byte (the XMLs are identical to the originals; do not edit them, not even the spacing): `indoor-lab-superclient-config.xml` (was `uf_fastdds_profile.xml`), `autonomy-park-superclient-config.xml`, and three netplan files named for their computers.
- Done: a camera-malfunction warning on Mocap Calibration (intermittent faults, as rare as one frame in 30 minutes).
- **Check:** Mocap Calibration, Networking Setup (Indoor Lab), Astro Overview table. 
- Max 2026-11-10 (follow-up): `MC_BAT_SCALE_EN` and `MC_AIRMODE` confirmed; `main.cal` made October 2025, "Exceptional"; `202.yaml` fixed (added `network:`); BPLJHL2 is .202, A0B is .203 and the discovery server; USW at .150 and U7 Pro at .18, so T-131 is done.
- Max:

### T-161 Max's eleventh batch (2026-11-10): NTRIP caster, AI for Debugging Jetsons, crash videos, wider layout, videos — `APPROVED`
- Max 2026-11-10: new Networking page NTRIP Caster for RTK on Quadcopters (from his `ntrip-caster-guide.md`; reference only, linked from RTK Setup); new Software page AI for Debugging Jetsons (from his SSH guide; linked from Jetsons). Both: headings without numbers, no comments in code, the example password replaced by `<password>`, robot IP and username replaced by placeholders.
- Crash videos converted with ffmpeg (muted, 1280x720, about 2 MB each, in Git LFS as `.mp4`): `docs/videos/homebrew-05-crash-2026-01-31.mp4` in the Lidar case study, `docs/videos/homebrew-03-crash-2026-10-09.mp4` in the MAVROS Link Saturation case study. Autoplay, loop, muted, dated captions.
- Wider pages: one CSS rule, only at screen widths of 1220 px and up, raises the content width to 80 rem. Below that nothing changes, so phones and tablets are untouched. Checked with a 1440 px screenshot. To undo, delete the last rule in `extra.css`.
- Video on Mocap Calibration and Bebop Autonomy (T-025, T-151 done). T-071 fine as is. T-096 assigned to Brandon. T-130 stays open.
- Max:

### T-159 Max's ninth batch (2026-11-10): Astro video, Upgrading ROS 2, verification dropped, ground_docker — `APPROVED`

Astro tutorial video on Flying Manually (linked from Autonomy; the page is now active); Software > Upgrading ROS 2; the Verified field is gone from the byline, hook and style guide (Max: only the date updated, and everything counts as verified); ground_docker warning on the Jackal, Go1 and B1 pages with Jackals marked not ready; T-151 added to the Indoor Lab list; Q88 and Q84 closed.

**How to verify:** Astro Flying Manually, Upgrading ROS 2, Jackal UGV, Go1, B1.

### T-158 Max's eighth batch (2026-11-10): parameters, payload, landing gear, RTK Setup — `APPROVED`

Parameters: SDLOG_PROFILE, MPC_THR_HOVER, MC_BAT_SCALE_EN, MC_AIRMODE added (all High) to the page and the .params; the .params also now has the earlier GPS and IMU Z offsets (it did not before this batch). Payload warning on the Homebrew Overview; landing-gear Known Issue; Astro Autonomy cross-publishing note; Homebrew RTK Setup rewritten as ordered steps (outdoors only).

**How to verify:** Homebrew Parameters (MC, MPC, SDLOG rows), the .params file, Overview, Known Issues, RTK Setup, Astro Autonomy.

### T-157 Max's seventh batch (2026-11-10): SITL button and note, Latest versions, video note — `APPROVED`

Home has an Autonomy Park SITL button; the SITL page says the repository is private; every Unknown version in Software We Use is "Latest"; the Homebrew video has the "okay to cut the case" note.

**How to verify:** open Home, Autonomy Park SITL, Software We Use, and the Homebrew Overview.

### T-156 Max's sixth batch (2026-11-10): renames, batteries, Passwords, Contribute removed — `APPROVED`

Networking pages renamed (Reserving a Static IP Address, File Backup Server, Networking Setup (Indoor Lab)); Astro and Homebrew Batteries pages; Use Our Web Resources became Passwords under Start Here > Access; Edit the Wiki moved into Start Here after Schedule a Time; Using an AI Agent deleted; the Contribute tab is gone (Home card now points to Edit the Wiki).

**How to verify:** check the nav, the Start Here table, and the two Batteries pages.

### T-155 Max's fifth batch (2026-11-10): Bebop Setup merge, Flight Practice, GitHub guide, Home photo — `APPROVED`

Bebop Setup merged into Overview; new Quadcopter Flight Practice (Liftoff) and GitHub Contribution Guide pages; Flying Manually buttons; Homebrew setup video embedded; Home gets a second photo; the byline no longer shows "Assisted by" or "Not yet verified" (draft banners stay).

**How to verify:** open Home, Bebop Overview, Quadcopter Flight Practice, both Flying Manually pages, GitHub Access, and any page's byline.

### T-154 Homebrew parameters import, Relevance column, soldering merge (2026-11-10) — `APPROVED`

Imported the Desktop parameter changes (GPS/IMU Z offsets, FRD note), added a Relevance column (High or "-") to every Homebrew Parameters table, merged the Soldering Tutorial into the Motor Soldering Guide, added the Bill of Materials button to the Homebrew Overview, and gave tables a full-width border so the right edge is not clipped.

**How to verify:** open Homebrew Parameters (EKF2 section, Relevance column), Motor Soldering Guide, Homebrew Overview, and Computing Hardware (right border).

### T-153 Max's fourth batch (2026-11-10): Homebrew restructure, Jetsons, numbers — `APPROVED`
- Done: Known Issues table fixed (the separator row had too few columns) with a homebrew_docker Set Up column and Ready to Fly by your rule; Lidar Cables is a danger box; full-RTK-fix danger box on the Astro and Homebrew Overviews (`snippets/rtk-fix-danger.md`); Homebrew RTK Setup says corrections are automatic once the three conditions hold; Jetson Orin Nano Firmware Flashing Guide merged into Jetsons and deleted; Radio and RC Setup Guide moved to Hardware; Set Up folder and its Overview removed, its pages moved to the Homebrew root, and its Pages table moved into the Homebrew Overview (now listing every Homebrew page); Docker Configuration renamed Autonomy; the "Boot Jetson with SSD" button removed (its link is on Jetsons); numbers removed from every heading (style guide and lint updated; "section 4.0" references now link by name); OS sentences now say Linux.
- The "(i)" after some nav titles is Material's page-status icon: it draws one after any page whose front matter has a `status` key (active, draft, and so on), because our `status` key has the same name as Material's.
- Parameter comparison (Desktop `homebrew_params.md` against Parameters): 202 parameters in both; seven differ (reported to Max in chat, nothing changed).
- **Open:** Q86, Q88.
- Max:

### T-149 Each robot's Overview must walk from hardware setup to manual operation and autonomy — `TODO`
- Max 2026-11-09: at some point every robot's Overview page should explain everything needed, from setting up the hardware (for example batteries) to manual operation and autonomy.
- Max:

### T-150 Back up the OptiTrack calibration file — `APPROVED`
- Max 2026-11-09: back up the calibration file for the OptiTrack setup (the repo has `docs/hardware/mae-a-313-calibration-2025-10-21.cal`; make a copy outside GitHub).
- Max:

### T-151 Write the Bebop Autonomy page — `APPROVED`
- **Max 2026-11-10:** Done: the video above, embedded on Bebop Autonomy (now active).
- Max 2026-11-09: `parrot-bebop-2/autonomy.md` holds only the notes moved out of Setup. Max writes the page.
- Max:

### T-146 Organize the subpages of every robot the same way — `APPROVED` (done 2026-11-06 with Max's OK, plus an Autonomy page type, new Hardware, Networking and Access tabs, and the file renames of T-042)
- Max 2026-11-06: robot subpages should be organized consistently. Examples: the Astro page has too many sections on one page; and the Freefly pages sit on the same level in the nav (Astro, Updating the AMC Version, Setting Up RTK on the Astros, Alta X, repairs), which is odd. My proposal for review: every robot gets a group in the nav with the same page types where they exist: **Overview** (the robot's main page: picture, fleet, manual), **Set Up**, **Operate**, **Maintain**, and separate pages for long sections (for the Astro: Dashboard, Parameters, Status Codes, MAVROS Installation, USB-C Port, Batteries). Groups by maker (Freefly, Clearpath, Unitree) get an overview page, with Alta X under "Retired". Do after the style sweep.
- Claude 2026-11-06: nav now: Home, Start Here, Robots, Hardware, Networking, Software, Access, Safety, Contribute (Infrastructure dissolved, Loaned Robots removed). Astro split into Freefly Astro (overview), Updating the AMC Version, Setting Up RTK on the Astros, Astro USB-C Port, Operate (Parameters, Dashboard, Status Codes), Astro MAVROS Installation, Astro Batteries. New maker overview pages Freefly, Clearpath, Unitree. Homebrew grouped Overview, Build, Set Up, Flying Manually, Homebrew Docker Configuration (Autonomy), Maintain, Case Studies. Old links are not redirected (Max). **Check:** the page placement in Hardware, Networking, Software and Access (list in the chat reply).
- Max:

### T-116 Style lint script and the end-game sweep — `DOING`
- Claude 2026-10-22: `tools/lint_pages.py` checks the mechanical rules of `meta/DESIGN.md` on every page (front matter, one heading theme, Title Case, ALL CAPS, numbered headings, body H1, standalone links, comments in code blocks, date format, canonical names). First run: 181 findings on 52 pages (mostly old pages not yet swept). The end-game sweep works from this list, then I read each page once for what a script cannot check. Run: `uv run python tools/lint_pages.py` (`--summary` for counts).
- Max:

### T-115 Parse `oct22-new-stuff/` — `APPROVED` (Emlid screenshots, Homebrew Case Studies, and flight history published 2026-10-22; "certified" dropped by Max on 2026-11-03)
- Max 2026-10-22: he added `oct22-new-stuff/` (local only, now gitignored with the other raw folders). **Contents and what I plan to do with each (Q43 decides):**
  - `Emlid RS3 *.png` (6 Emlid Flow screenshots): these are the T-074 screenshots. They show: Receivers home (Wi-Fi SSID `UFLAutonomyPark`, correction input off, Base output 1 TCP server, base output 2 LoRa), Settings, Base output 1 (TCP server `localhost:9000`; the LoRa option says the radio is used by output 2; Local NTRIP `192.168.1.13:2101`; RTCM3 format), Base output 2 (LoRa radio 920.0 MHz, 18.23 kb/s), RTCM3 messages (1006 at 0.1 Hz; 1074, 1084, 1094, and 1230 at 1 Hz; 1124 BeiDou off), and Base settings (manual coordinates, antenna height 2.174 m, base marker coordinates). Plan: process the images (crop, alt text, LFS) and write a "Emlid Flow Settings" section on `infrastructure/rtk.md` with the values as a table. **Check first:** the Base settings screenshot shows the base marker's exact latitude and longitude (the Park's tower location). I think the location is not sensitive (the Park is on public maps), but you decide (Q43).
  - `Homebrew Flight Logs.rtf` (your per-Homebrew flight log, January to October 2026): plan to turn it into per-Homebrew history on the Homebrew Fleet page (certified or not, crashes, firmware, dates), plus lessons for Cursed Knowledge: (1) MAVROS with all plugins on saturates the 40 to 64 KB/s serial link between the Jetson and the flight controller, giving an RTT of 2500 ms and old state data; Homebrew 03 crashed into the net on 2026-10-09 because of it; (2) the lidar and CAN burnout from non-standard cabling (use I2C 2 and the included cable); (3) the lidar flicker explanation (two distance sensors on one CAN); (4) the vibration and canopy-mount tests; (5) Homebrew 05's hard fault. **Conflicts to resolve (Q43):** the log says Homebrew 10 was never flown, but your crash list says 10 has crashed; the log mentions people by first name (Damian, Brandon, Jordan, Vikram), which I would leave out of the public page.
  - `px4_param_porting_case_study.md` (2026-10-22, PX4 `main` with PR #29368 on a Homebrew): plan to publish as a page under Homebrew, "PX4 Parameter Porting Case Study", linked from Upgrading PX4 Firmware, keeping its warnings (not for 1.18.0 or any stable release; the method matters, not the answers). Its checklist feeds the upgrade page (T-052/T-014). Also resolves facts I have recorded as unknown: the 1.17-dev `main` parameter renames and removals.
  - `homebrew_params_rtk_test.md` and `.params` (the `main` port, 194 parameters, valid only for commit `5f429033bf` and the PR branch): **risky to publish as a template**, since someone could load it on 1.16.2. Plan: publish only as clearly labeled examples on the case-study page, behind a danger box, not in the Files table of PX4 Configuration (Q43).
- **Follow-ups this unlocks:** T-074 (screenshots received), T-062 (RTK page: base settings, RTCM message rates, two base outputs), T-110 (LoRa 920.0 MHz settings known; which robots carry an Emlid unit is still Wyatt's), T-112 (fleet history).
- Claude 2026-10-22: Max answered Q43 (a) to (d): publish the base coordinates; Homebrew 10 was crashed by Brandon Fallin and Jordan Insinger before Max took over flight tests; keep names; the `main` parameter files go under a new Homebrew subsection **Case Studies**. Done: `case-studies/` has five pages (Porting Parameters to PX4 Main, Example Parameters for PX4 Main with a danger box, MAVROS Link Saturation, Lidar and CAN Burnout, Position Mode Instability); the Fleet page has a Flight History table and updated notes for Homebrew 03, 05 and 10; RTK Setup has the Emlid Flow settings table and six screenshots (`md_in_html` enabled for the image grid); Upgrading PX4 Firmware links the porting case study. **Case studies are written from your notes only, with `Unknown` where the log is silent. Please read them for factual errors and say if you want the other one or two case studies you mentioned.**
- Claude 2026-11-03: applied Max's review of the four case studies: titles quoted (a colon broke the front-matter title), PR #29368 marked merged (likely 1.19.0), `COM_KILL_DISARM` deep dive cut to a short note with the 5 s landing warning, calibration parameters survived the test flight, firmware built and flown (see the PR), PR and issue numbers hyperlinked, MAVROS page links `homebrew_docker` and `autonomy_park_sitl` and notes control barrier functions do not exist yet, two lidar wiring photos added, Cursed Knowledge Homebrews section removed (Max). **Open for Max:** the list "Not recorded as verified" on the porting page (antenna offsets, `EKF2_SENS_EN`, GPS with GNSS 1 off, arming below RTK fixed, issue #29346): which of these did the flights verify?
- Max:

### T-114 Bebop Fleet table without IPs — `APPROVED`
- Max 2026-10-21: removed the IP column from the Bebop hardware-problems table (`bebop/fleet.md`); IPs stay on IP Reservations; the "At a glance" and pointer sentences fixed.
- Max:

### T-111 LiPo Battery Safety lists, and one heading theme everywhere — `APPROVED` (rule written; the lists question is still open in Q41(a); sweep at the end)
- Max 2026-10-21 accepted my proposal: Title Case only, numbers only on the two SOPs, PX4 Configuration, and Flying Manually, steps as list items not headings, and (my addition, from the TOC finding in T-107) no body `# H1`. The rule is in DESIGN §11. **My addition needs your OK:** the no-body-H1 line; strike it if you disagree.
- Max 2026-10-21: "First the lists in Lipo Battery Safety" (the sentence was cut off; see Q41), and make sure all section headers use a consistent theme everywhere; add it to the style guide. Observed today: the SOP pages use numbered ALL CAPS headings (`1.0 PURPOSE`, `4.0 INSPECTION`), the PX4 pages use numbered Title Case (`4.0 Clean Configuration Procedure`), tutorials use `Step 1:` or unnumbered Title Case, and many pages have no numbers. My plan: write the rule into DESIGN §11 as soon as Max picks it, and apply it with the end-game heading work (T-107, T-038, T-040), since all of them change headings and the table of contents.
- Max:

### T-110 Wyatt finds which ground robots have an Emlid unit — `AUTHOR-TBD` (Wyatt Cross)
- Max 2026-10-21: Max does not know which ground robots have an Emlid unit (and so use LoRa instead of the RTKLib caster). Task for Wyatt: for each ground robot (Husky A200, Jackal UGV, Go1, B1; ROSbot is Indoor Lab only), say whether it carries an Emlid unit, which model, and its LoRa settings. Result goes on `infrastructure/rtk.md` (the section "How Corrections Reach the Robots") and the robot pages; ties to the Emlid inventory (T-053). Max to ask Wyatt.
- Max:

### T-109 RTK Setup: two ways corrections reach the robots — `APPROVED`
- Max 2026-10-21: ground robots with an Emlid unit (e.g. an RS) use LoRa radio; all others use the RTKLib caster. The split was chosen to minimize changes to existing configurations, not because Wi-Fi or the caster would saturate with many agents (not known). Done on `infrastructure/rtk.md` (new section, glance updated). Which ground robots have an Emlid unit, and the LoRa settings: Wyatt (T-110).
- Max:

### T-108 Every robot has tags, and the style guide says so — `APPROVED` (see Q40)
- Max 2026-10-21: make sure all robots have tags; add this to the style guide. I am not sure which tags: page tags in the wiki, or physical asset tags/decals on the robots. Waiting for Q40 before changing anything. When decided: the rule goes in `meta/DESIGN.md`, every robot page gets checked against it, and (if page tags) the Material `tags` plugin is enabled with a tag index page.
- Max:

### T-107 End-game: verify the table of contents on every page — `LAST` (Claude)
- Max 2026-10-21: verify that all tables of contents are properly tracked on all pages. Example: "Batteries" shows a TOC but "Configuring the WiFi on Bebops" does not. First look (not a conclusion): both built pages contain TOC markup, but the Bebop Wi-Fi page starts with its own `# H1` heading and numbers its steps as `###` under `##` steps, while Batteries has no `# H1` and a single `##` heading. Hypothesis: pages with a body `# Title` get the TOC nested under that title, which looks like no TOC. At the end: build the site, list every page's TOC entries, find pages with none, one, or oddly nested entries, and fix the headings (one convention: no body H1, since the page title is shown by the theme; headings start at `##`; steps as list items, not headings). Do it with T-038/T-040, after the content is stable.
- Max:

### T-106 Bebop battery table, and the table-date rule — `APPROVED`
- Max 2026-10-21: removed the Cycles column from the Bebop battery table and added a Last Updated column (`2025-08-21`, the sheet's date), last, ISO format like the Bebop Fleet table; the rule is in DESIGN §8 (Last Updated is the last column, dates as YYYY-MM-DD). **Sweep still to do (with T-031):** `asset-management.md` writes dates as `07/08/2026`; I do not know if that is 7 July or 8 July, so I did not convert it (Q38). Other tables get a Last Updated column only where they track state.
- Max:

### T-105 Label every Homebrew battery and give it a cycle tracker — `APPROVED` (Autonomy Park)
- **Max 2026-11-10:** Done to Max's satisfaction.
- Max 2026-10-21: make sure all Homebrew batteries are labeled and have cycle trackers. Max will take a picture of the label and tracker. Needs Max at the Autonomy Park (battery sheds): count the Homebrew batteries, label each, add a cycle tracker. Then I add the picture and what a good label and tracker look like to `safety/batteries.md` and the Homebrew pages, and record where cycle counts are kept (the Bebop batteries page says Bebop cycle counts are unknown, a similar problem).
- Max:

### T-104 Note at the top of "Configuring the WiFi on Bebops": for reference only — `APPROVED`
- Max 2026-10-21: all working Bebops should already be connected to the Indoor Lab LAN; the tutorial is provided only for reference. Done: a `note` as the first thing on `bebop/configure-network.md`; its "At a glance" sentence says the same.
- Max:

### T-103 Every Autonomy Park robot page tells the user to set up the RTK ground station first — `APPROVED`
- Done 2026-10-21 (Max: skip the Alta-X; the Husky A200, Jackal UGV, Go1, and B1 all use RTK): a note from the shared snippet `snippets/rtk-first.md` plus an `RTK Setup` button at the top of `how-to-fly`, `homebrew-reference`, `homebrew-docker`, Astro, Husky A200, Jackal UGV, Go1, B1, and `safety/quadcopters.md`. The button sits under the snippet because the relative link differs by folder depth. Original task text follows.
- Max 2026-10-21: for all Autonomy Park robots, the user is first told to set up the RTK ground station, with a button link to RTK Setup (`[RTK Setup](../../infrastructure/rtk.md){ .md-button }`, relative path per page). Put it at the top of each page as one shared snippet (`snippets/`), so the wording is in one place. Pages: Homebrew (`how-to-fly.md`, `homebrew-reference.md`, `homebrew-docker.md`), Astro, Husky A200, Jackal UGV, Go1, B1, and the safety pages for flying (`safety/quadcopters.md`). Not the Indoor Lab robots (Bebop, Starling 2 Max, ROSbot). See Q37 for the Alta-X and the pages where RTK may not apply.
- Max:

### T-102 Remove Ground Robot Setup Videos; controller colors; Starling 2 Max page — `APPROVED`
- Max 2026-10-21: (1) `ground-robot-startup.md` is removed (its videos already live on the Husky A200, Go1, and B1 pages, and the Emlid one moved to the RTK page); the old URLs redirect to the home page; nav entry removed. (2) Wireless Controllers table has a Color column: the Autonomy Park DualSense is white, all others black. (3) New empty page `robots/quadcopters/starling-2-max.md` (Indoor Lab only, draft banner, nav entry above Bebop), with the glance Max asked for (his wording lightly fixed: "Starling 2 Maxes"). It relates to T-049.
- Max:

### T-100 Wyatt makes a startup video for the Clearpath Jackal UGV — `AUTHOR-TBD` (Wyatt Cross)
- Max 2026-10-21: Wyatt to make a startup video for the Jackal UGV (the Husky A200 has one). When it exists, it goes on `clearpath/jackal-ugv.md` and `ground-robot-startup.md`, with a text summary (DESIGN §7). Max to ask Wyatt.
- Max:

### T-101 Clearpath pages: manuals as buttons, IP reservations removed, new names — `APPROVED`
- Max 2026-10-21: removed the IP reservations (and the password column) from the Husky and Jackal pages; both manuals are buttons with Max's corrected links; the Husky is called **Husky A200** and the Jackal **Jackal UGV** everywhere (titles, nav, glance, jetsons, asset management, startup videos; device hostnames like `Husky706` stay); the Go1 is said to be the smaller dog and the B1 the larger. Files renamed to `husky-a200.md` and `jackal-ugv.md` with redirects (DESIGN §12). Names are in DESIGN §3.
- Max:

### T-099 Harness page under Unitree — `APPROVED`
- Max 2026-10-21: take the Harness section away from the B1 and Go1 pages and make it its own minimal page under Unitree: the harness can be used with the Go1 or B1 to test a low-level motor controller (e.g. RL) on the dog safely before having it work on its own; no one has ever done this; the metal needed to assemble it is in the Indoor Lab. Done: `robots/ground-robots/unitree/harness.md` (draft; nav entry), the harness manual as a button, the section removed from both dog pages and their glance sentences fixed. Whether it is Indoor Lab only: I set `applies_to: [indoor-lab]` because the metal is there; tell me if wrong.
- Max:

### T-095 Make all manuals buttons — `TODO`
- Max 2026-10-21: every manual link (for example the Go1 manual) becomes a button: `[Go1 Manual](go1-manual.pdf){ .md-button }` (with `download` where it should save). Applies to the vendor-manual links on Go1, B1, Husky, Jackal, Homebrew (Tattu, lidar), Freefly (Alta-X, charger, Futaba), and the harness manual. Part of the button rule (T-069); do it with that sweep.
- Max:

### T-096 Someone to confirm the Go1 Static Transforms are still relevant — `AUTHOR-TBD` (Brandon Fallin)
- **Max 2026-11-10:** assigned to Brandon; a note on the Go1 page asks him.
- Max 2026-10-21: `robots/ground-robots/unitree/go1.md` has a "Static Transforms" section for "the old dog hardware" (`minimal_startup_ground/launch/transforms.launch.py`). Max does not work with the robot dogs and does not know whether it is still relevant. Needs: someone who works with the dogs (Brandon?) to confirm or remove. Until then it stays as is, and I may add a "not confirmed" note if Max wants one.
- Max:

### T-097 Dog ROS 2 Startup Instructions need Brandon — `AUTHOR-TBD` (Brandon Fallin)
- Max 2026-10-21: the "Dog ROS2 Startup Instructions" section of `go1.md` says "Coming soon". It needs Brandon to write it. Max to ask him.
- Max:

### T-094 Log the netplan files for the Indoor Lab PCs — `APPROVED` (Indoor Lab)
- Max 2026-10-21: collect the `netplan` files from each Indoor Lab PC (`/etc/netplan/`) so the wiki records them. Needs Max at each PC. I will put them on `indoor-lab-computers.md` (Networking Setup) as a page of their own or a download. Check each file for Wi-Fi passwords and keys before it is committed (public repo; they are never published).
- Max:

### T-093 Parse the Google Drive files in `Relevant Google Drive Files/` — `APPROVED` (first batch; see Q35)
- **Done 2026-10-21 (Q34 answers applied):** `infrastructure/ip-reservations.md` (Park and Indoor Lab; the device login omitted; base station named RS3; hostnames shown); `robots/quadcopters/bebop/fleet.md` (20 Bebops with IP, LED color, notes, dates, and the Bebop 2 manual as a download button, PDF not read); Bebop battery table added to `bebop/batteries.md`; `infrastructure/jetsons.md` (T-024, draft); Astro status codes already match `astro.md`. **Not published:** serial and decal numbers (Max), and the device login. The raw folder stays gitignored. Original notes follow.
- Max 2026-10-21: he added the relevant Drive files for me to start parsing. The folder is local only and now gitignored (with the NDAA PDF), because some files hold sensitive data. Files: `IP Reservations - Autonomy Park.xlsx`, `IP Reservations - NCR Lab.xlsx` (the Indoor Lab; the file name still has "NCR", T-029), `Bebop Batteries.xlsx`, `Decals and Serial Numbers.xlsx`, `Astro Status Codes.xlsx`, `Parrot Bebop 2 Manual.pdf`.
- **First pass (read only, nothing copied into the repo yet):**
  - Park IP sheet: computers, sensing devices, the tower base station, Clearpath, Unitree and Freefly robots, and Jetsons, each with a reserved 192.168.1.x address. **One note in it holds a device login. It must never be published** (public repo; DESIGN §9), so the migration drops it. The Emlid base station there is called an **RS3+**; `infrastructure/rtk.md` says RS3 (Q34).
  - Indoor Lab IP sheet: four computers (one UFIT-managed, one mocap computer, one alternate ROS workstation, one discovery server) and Bebops 101 to 120 with LED color, hardware notes, and last-updated dates (2025 to 2026).
  - Bebop batteries: 16 batteries with swelling flags and notes (numbers 101 to 114 and 201 to 203; missing numbers were discharged).
  - Decals and serial numbers: serials and University decal numbers for computers, Clearpath, Unitree, Freefly, and Velodyne pucks.
  - Astro status codes: MAV_STATE values 0 to 8 (already public MAVLink definitions; `astro.md` has a Status Codes section to compare).
- **Plan (T-015 is now unblocked):** IP reservations become a table page under Infrastructure (the addresses, not the login); Bebop batteries and statuses go on the Bebop pages (T-022); serials and decals only with Max's OK (Q34); Astro status codes are checked against `astro.md`; the Bebop manual stays a vendor PDF beside the Bebop page. Each step is a small commit with Max's review.
- Max:

### T-092 Verify the Wireless Controllers tutorials on hardware — `DONE` (Max verified 2026-10-21; the "Not yet verified" notes are removed)
- The pairing, `joy` node, and button-mapping steps on `wireless-controllers.md` come from standard `bluetoothctl` and ROS 2 Humble usage, not from lab runs; they carry a "Not yet verified" marker. Max: run them with a DualSense on a lab Ubuntu computer (Indoor Lab or Park), then tell me what to fix (e.g. exact pairing-mode buttons, controller name in the scan list).
- Max:

### T-091 Wireless Controllers: why DualSense beats Xbox for robotics — `APPROVED`
- Max 2026-10-21: document why PS5 DualSense controllers are better than Xbox controllers for robotics, titled **Wireless Controllers**; our inventory (one DualSense in the Indoor Lab and one at the Autonomy Park, never to be removed; two Xbox 360 Wireless in the Indoor Lab with stick drift; both DualSense bought September 2026); both are supported by ROS 2 (`joy` node); Xbox has no out-of-the-box Linux Bluetooth (firmware upgrade Windows-only, our attempt failed, rapid connect-disconnect); DualSense works over Bluetooth in the kernel; why Bluetooth matters; the DualSense firmware upgrade also failed on Windows. Done: `robots/wireless-controllers.md` with both stock images, nav entry under Robots (my placement; move it if you prefer). The stock images are vendor product images (Q25). Max 2026-10-21: Xbox Wireless Controller means the third revision; the Park's third-revision controller broke and was thrown away (the 2 in the Indoor Lab are the 360s); added the DualSense Bluetooth pairing on Ubuntu, the joy node, and the button-mapping tutorials.
- Max:

### T-090 Tutorial: requesting admin access to the University-managed Indoor Lab PC — `APPROVED`
- Done 2026-10-21 from Max's steps: `infrastructure/indoor-lab/requesting-admin-access.md` (talk to Dr. Kamalapurkar first, then the UF Engineering IT ticket; applies to both UFIT-managed computers). Linked from IP Reservations. Original task text follows.
- Max 2026-10-21: write a tutorial for requesting admin access to the one PC in the Indoor Lab that is University-managed. Needs Max: which PC, who to request from, the steps and form, and what to expect. Related to T-085 (which Indoor Lab computers are University-registered). Goes on `infrastructure/indoor-lab/indoor-lab-computers.md` or its own page under Indoor Lab. Do not publish the PC's asset tag, serial number, or any account names without Max's OK.
- Max:

### T-089 Empty ROSbot 2 Pro page under Ground Robots — `APPROVED`
- Max 2026-10-21: an empty page for the ROSbot 2 Pros, author Muzaffar Qureshi (spelling as Max wrote it), with the ROSbot picture, a caption, and a message asking for his help, nothing else. Done: `robots/ground-robots/rosbot-2-pro.md` (title "ROSbot 2 Pro", singular; draft status banner; nav entry under Ground Robots). The picture is the vendor product image (see T-088 and Q25); it is now used. Content is Muzaffar's to write (T-026).
- Max:

### T-088 Add a picture to each robot's page — `APPROVED`
- Max 2026-10-21: add pictures from `possible_assets/Robots/` to each robot's page. Available: Husky, Jackal, Alta, Astro, Homebrew (and Homebrew Parts), Bebop 2 (and two propeller-tool photos), ROSbot 2 Pro, TurtleBot4, Unitree B1, Unitree Go1. Process each like the other images (check for people, resize to 1600 px or less, `.jpg`, LFS, alt text, `images/<topic>/`). **Checks before publishing:** several look like vendor product images (copyright, as with the RS3, Q25); pages for ROSbot and TurtleBot4 do not exist yet (T-026), so those pictures wait (ROSbot: done by T-089); the Homebrew hub page and a Bebop hub page may need to be created for a picture to land. Where a page already has a picture, I keep it and say so.
- Claude 2026-11-06: added a picture to Husky A200, Jackal UGV, B1, Go1, Astro, Alta-X, Parrot Bebop 2 (Fleet page) and Homebrew (Quick Reference). Husky, Jackal, B1, Go1, Astro, Alta-X and Bebop are manufacturer product images (captions say so); the Homebrew is the lab's own photo, with the orange sticker on its canopy blurred (no decal numbers). ROSbot already had one. Not used: `TurtleBot4.jpg` (no page), `Go1 Harness.png` (looks like a harness from another lab: tiles and wall are not ours), `Homebrew Parts.jpg`, the two Bebop propeller-tool photos (no page uses them yet). Starling 2 Max stays empty.
- Max:

### T-087 Merge "Software We Use" and the ROS 2, MAVROS, PX4, and QGroundControl installation page — `APPROVED`
- Done 2026-10-21 (Max: single page, Lab Notes): `software.md` keeps its table and gains a Lab Notes section (Ubuntu and VM disk space, ROS 2 test, QGC, Gazebo, PX4 SITL, the uXRCE-DDS note, MAVROS, Troubleshooting); each row links to its note; `simulation-installation.md` is removed with redirects. **Removed as duplicates of the vendor guides** (still in git history, `git show HEAD~1:docs/start-here/software-setup/simulation-installation.md`): the ROS 2 Humble install commands and the Gazebo Harmonic install commands. Everything else was kept. **Please check** that nothing lab-specific was lost in those two. Byline now Max and Brandon Fallin (both authors of the merged pages). Old task text follows.
- Max 2026-10-21: merge `start-here/software-setup/software.md` and `simulation-installation.md`. No repeating of vendor install guides (for example the ROS 2 Humble installation steps); keep the lab's tips from the installation page. Max likes the table as it is. My recommendation is in Q31. When decided: move the tips, delete the installation page with a redirect (`redirects.yml`), fix every link to it, update the nav, the "Used On" column, T-079, and the QGC warning snippet's placement (T-057). The MAVROS-to-uXRCE-DDS note and the RTK facts on the installation page (T-046) must survive the move.
- Max:

### T-086 Explain where the Autonomy Park bathroom is — `APPROVED` (Max)
- Max 2026-10-21: write where the bathroom for the Autonomy Park is. Known from `access-requests.md`: bathroom access is in the Student Design Center at the Solar Park (room 0980), requested with the second form. Needs Max: directions from the Park (where to park or walk, which door), and a photo or map if useful. Goes on `lab-spaces-and-dimensions.md` (Autonomy Park section), linked from Access Requests.
- Max:

### T-085 Explain which Indoor Lab computers are University-registered and which are not — `APPROVED` (Max)
- **Max 2026-11-10:** Done already (Max).
- Max 2026-10-21: write down which Indoor Lab computers are University-registered (UF-registered) and which are not. Needs Max: the list and what the difference means in practice. Goes on `infrastructure/indoor-lab/indoor-lab-computers.md` and the Computing Hardware page. Do not publish identifiers like asset tags or serial numbers without Max's OK.
- Max:

### T-084 Back up the mocap calibration file — `APPROVED`
- Max 2026-10-21: added `Mocap/` (gitignored) with the calibration file (made 2025-10-21, mean error 0.854 mm) and the Motive 2.0.2 installer. Done: the `.cal` is committed as a download on `mocap-calibration.md`. Installer deliberately not committed (Q36). Motive facts and the license-key danger and button are on that page. Original task text follows.
- Max 2026-10-21: back up the OptiTrack Motive calibration file for the Indoor Lab. Needs Max at the Indoor Lab. Open: where the backup lives (and the file must not go in the public repo if it carries anything sensitive); once it exists, say on `mocap-calibration.md` where it is and how to restore it (T-025).
- Max:

### T-083 Download for the Autonomy Park discovery server configurations — `MAX-TBD`
- Max 2026-10-21: add a download of the discovery server configurations for the Autonomy Park (a file Max attaches, linked with `{ download="..." }` as a button, T-063). Needs Max: the file(s), and which page they belong on (probably the RTK Setup page or a new discovery-server page under Infrastructure). Check the files contain no passwords, keys, or other secrets before they are committed (public repo).
- Max:

### T-081 Decide what to do about Brandon's "The slide deck for this SOP can be found here" — `APPROVED`
- **Max 2026-11-10:** Resolved: Max removed the SOP slide-deck line completely.
- Max to decide. `safety/quadcopters.md` line 15 links the SOP slide deck PDF (`quadcopter-sop.pdf`). The PDF lacks the new flight-modes and battery warnings (T-037), and DESIGN §7 says a slide deck may stay a PDF only if the page holds the full text too. Options: keep the link as is; replace it with a note that the deck is out of date; remove the deck and the sentence.
- Max:

### T-077 Document downloading the firmware from QGC's Firmware tab — `DROPPED` (Max 2026-11-06: people build it with Building PX4; no need for a QGC download)
- Max 2026-10-21 (Q26b): it needs a drone: a flight controller connected via USB. Max to do the procedure and record it (screens and steps), for `upgrading-firmware.md` step 1 and `px4-configuration.md` section 6.1. The page currently says the steps are *Not yet documented*.
- Max:

### T-078 Astro and Alta-X: Freefly and the XRCE-DDS Agent — `APPROVED` (2026-11-03: Freefly says the Astros do NOT support it; Max removed the Alta-X note as not relevant)
- Max 2026-10-21: Freefly confirmed over support that their platform supports the Micro XRCE-DDS Agent for torque-level offboard control. Done: a note on `astro.md` and `alta-x.md`. Needs Max: who at Freefly, when, and whether it applies to Gen 1 Alta-X as well as the Astro (I wrote "the platform", as you said).
- Max:

### T-079 Software We Use: download links, docs column, and the "Used On" column — `APPROVED` (Used On audited against page mentions 2026-11-06; main omissions added)
- Max 2026-10-21: "Official site" became a **Download** column (direct install or release pages), and a separate **Docs / Homepage** column was added. Rows added: RTKLib 2.4.3, Emlid Flow. "Used On" updated for pages written this session. I checked that every link answers (a few vendor sites block scripts: OptiTrack, Emlid). The Emlid Flow download link is Unknown.
- **End-game (me):** audit that every row's version, download link, and "Used On" list is accurate against all pages (grep each software name across `docs/`), and that every software name used anywhere has a row. Do this with T-038/T-040.
- Max:

### T-076 Make the GitHub organization link a button on the home page — `APPROVED`
- Max 2026-10-21: done on `docs/index.md` (button below the intro paragraph). Part of the button rule (T-069).
- Max:

### T-075 Title Case everywhere — `APPROVED`
- Max 2026-10-21: all titles capitalized consistently, and the rule is in `meta/DESIGN.md` §11. Done: rule written; every heading in `docs/` swept (case only, anchors unchanged); page titles and nav labels already conform. New pages follow the rule.
- Max:

### T-074 Screenshot the Emlid Flow settings — `APPROVED` (screenshots and settings table are on RTK Setup, 2026-10-22)
- Max: screenshot the Emlid Flow (mobile app) settings for the ground station and the rovers: rates of corrections, what to set updates to, and so on. Goes on `infrastructure/rtk.md`.
- Max:

## E. New tutorials and real-world TODOs

### T-025 Motion capture (OptiTrack Motive) tutorial + robot frames — `APPROVED`
- **Max 2026-11-10:** Done: the video https://youtu.be/2qiJW6F9iWw covers the mocap tutorial (and `bebop_common`); embedded on Mocap Calibration and Bebop Autonomy.
- Setting up Motive, calibration (exists: `infrastructure/indoor-lab/mocap-calibration.md`), creating rigid bodies and coordinate frames for robots. Needs Max's **screenshots from Motive in the Indoor Lab**.

### T-026 RosBot tutorials — `APPROVED`
- **Max 2026-11-10:** Done (Max).
- Not listed anywhere yet. Max to ask someone to write. Indoor Lab only. I will create the page skeleton and an "authors wanted" status.

### T-029 Rename Drive IP-reservation documents and obtain SOP source — `MAX-TBD`
- See T-005. Needed before the last NCR mentions can go.

### T-027 Check the Indoor Lab Wi-Fi SSID — `APPROVED`
- Max 2026-11-09: also fill in the correct SSID on Connecting to WiFi (Bebop), where it says Unknown.
- Is the Indoor Lab SSID still `NCRLab` (renamed in 2025)? Blocks the SSID wording in T-005.

---

## Questions for Max (open)

| # | Question | Needed for |
|---|---|---|

Answered: Q37 (skip the Alta-X; all the ground robots use RTK), Q36 (yes to all: 2.0.2, the calibration file is public, capital hostnames), Q35 (removing the name is OK), Q36 part (admin access applies to both UFIT-managed computers; the Motive installer is a Drive download, not in the repo), Q35 part (the sheet is correct: two UFIT-managed computers; .201 is Windows 11; yes, the wiki's battery and fleet tables replace the Google Sheets), Q34 (Jetsons get their own page, no serial numbers published, hostnames of University-managed computers OK, the base station is an RS3 and RS3+ is not a real model), Q33 (the two Xbox controllers in the Indoor Lab are the 360s; the Park's third-revision Xbox Wireless Controller was thrown away), Q32 (2 Xbox Wireless in the Indoor Lab; the broken one was the third revision; pairing and joy tutorials wanted), Q31 (single page with Lab Notes), Q30 (folder renamed too; short Safety First page in Start Here; safety stuff moved out of Access Requests, with a loud pointer), Q29 (the 30-50-70 throttle step is fine as written), Q27 (cabinet text fine, jaws spread, inside = main shed, never off-premises, public OK), Q25 part (picture fine), Q21 (labels confirmed), Q23, Q24, Q19, Q2, Q5, Q12 to Q15, Q18, Q6 (renames approved and done), Q8 to Q11, Q16, Q17 (see T-014), Q7 (Systems, Cognition, and Control (SCC) Lab), Q1 (public IPs/SSIDs/routers/rooms fine), Q3 (personnel = Max, Opeyemi, PI; UF emails + photos), Q4 (SSID unknown, now T-027).
