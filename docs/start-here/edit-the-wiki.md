---
title: Edit the Wiki
author: Max Gardenswartz
updated: 2026-10-21
status: active
assisted_by: Claude
glance: >-
  All users of the Autonomy Park and the Indoor Lab are expected to track their hardware issues, document useful facts, and correct errors in this wiki. This guide teaches how to edit it.
---

This wiki is a folder of Markdown files in a GitHub repository. [MkDocs](https://www.mkdocs.org/) with the [Material](https://squidfunk.github.io/mkdocs-material/) theme turns them into the website. Pushing to the `main` branch publishes the site automatically.

## Requirements

You need three tools.

| Tool | What it is for |
|---|---|
| [Git](https://git-scm.com/) | Versioning and sharing your changes |
| [Git LFS](https://git-lfs.com/) | Stores large files (PDFs, photos, videos) outside the normal Git history |
| [uv](https://docs.astral.sh/uv/) | Installs the correct Python and every package the wiki needs, at exact locked versions |

You do **not** install Python or MkDocs yourself. `uv` does that for you. Everything on this page runs on your own computer.

=== "Linux / WSL"

    Install Git and Git LFS:

    ```bash
    sudo apt install git git-lfs
    ```

    Install uv:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "macOS"

    Install all three tools:

    ```bash
    brew install git git-lfs uv
    ```

=== "Windows"

    Install Git. This also installs Git LFS:

    ```powershell
    winget install --id Git.Git -e
    ```

    Install uv:

    ```powershell
    winget install --id astral-sh.uv -e
    ```

Turn on Git LFS. Do this once per computer:

```bash
git lfs install
```

Check that all three tools respond with a version number:

```bash
git --version
git lfs version
uv --version
```

!!! warning "Turn on Git LFS before you clone"
    Without Git LFS, PDFs and photos download as tiny text files, and any large file you add goes into the normal Git history, where it stays permanently and slows down everyone's clones. See [Large Files (Git LFS)](#large-files-git-lfs).

## Get the Wiki

You need access to the [UFL-Autonomy-Park](https://github.com/UFL-Autonomy-Park/) GitHub organization. Ask one of the people on the [Contacts](contacts.md) page to add you.

Clone the repository:

```bash
git clone https://github.com/UFL-Autonomy-Park/apark_wiki.git
```

From here on, run every command inside the `apark_wiki` folder. Enter it and install the exact package versions the wiki uses. This creates a private environment in `.venv/`:

```bash
cd apark_wiki
uv sync
```

Preview the site on your computer:

```bash
uv run mkdocs serve
```

Open <http://127.0.0.1:8000/>. The page reloads every time you save a file. Stop the server with `Ctrl+C`.

!!! note "Read the terminal output"
    The preview prints `WARNING` lines in the terminal for broken links and missing files. Fix them before you push. A clean build prints none. The boxed notice from the Material team about MkDocs 2.0 is expected and is not about our site.

## Change or Add a Page

Pages are `.md` files under `docs/`. Each folder is a section in the sidebar. To add a page, put a new `.md` file in an existing folder, or create a folder for a new section.

Start every page with a title block:

```yaml
---
title: Your Title Here
---
```

For Markdown syntax, see the [Markdown Guide](https://www.markdownguide.org/). For boxes such as notes and warnings, see the Material [admonitions reference](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

### Links, Images, and PDFs

Use paths relative to the page you are editing.

A PDF sits in the same folder as the page that uses it and is linked by file name:

```markdown
[Battery Manual](tattu-manual.pdf)
```

An image goes in `docs/images/`, in a folder named for its topic. From a page in `docs/start-here/`, the path looks like this:

```markdown
![Autonomy Park robots](../images/index/robot-banner.jpg)
```

Count the `../` by how deep the page is. A page in `docs/robots/quadcopters/homebrew/` needs `../../../images/` at the start of the path. If an image does not show up in the preview, the number of `../` is almost always the reason. Always write alt text (the text in the square brackets) that says what the picture shows.

Another page is linked by its `.md` file:

```markdown
[Configure the Bebop network](../robots/quadcopters/parrot-bebop-2/connecting-to-wifi.md)
```

## Large Files (Git LFS)

Git LFS keeps the repository small. These file types are stored with LFS automatically, as listed in `.gitattributes`:

`.pdf` `.jpg` `.mp4` `.mov` `.heic` `.avif`

Use one format per kind of file: photos as `.jpg` (1600 px or less on the long side), screenshots as `.png`, diagrams as `.svg`, videos as short muted `.mp4` clips (longer videos go on YouTube), and vendor manuals as `.pdf`. Never use `.webp`.

If you turned on Git LFS (see [Requirements](#requirements)), you do nothing special. Add the file and commit as usual.

- Save photos as `.jpg` (not `.jpeg`) and resize them to about 1600 pixels on the long side before adding them.
- Export a real `.jpg` from your photo tool. Renaming a `.jpeg` file does not convert it.
- Anything that is not one of the types above, such as `.png` screenshots, stays in regular Git. Keep those small.

To confirm a new file went into LFS, list the LFS files. Your file should appear:

```bash
git lfs ls-files
```

!!! warning "A PDF or image shows as a few lines of text"
    The file is an LFS pointer, which means the real file was never downloaded. Download it:

    ```bash
    git lfs install
    git lfs pull
    ```

## Publish Your Changes

Stage all changes

```bash
git add 
```

Commmit changes

```bash
git commit -m "docs: <what you changed and why>"
```

Push changes

```bash
git push -u origin <branch-name>
```
- **Write what and why** in the commit message. Start it with `docs:` for content, `fix:` for corrections, or `feat:` for new sections in the style of [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#specification).
- **Update the page when you change a robot.** If you changed a robot's configuration, network, or software, document it here. Anyone who inherits the robot depends on it.
