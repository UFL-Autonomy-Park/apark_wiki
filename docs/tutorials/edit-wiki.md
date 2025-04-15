---
title: Edit the Wiki
---

## Requirements

To edit the wiki, you will need `python` and `mkdocs`. Download Python [here](https://www.python.org/downloads/).

Once you have Python installed, install pip (package manager for Python):

```
python get-pip.py
```

[MKDocs](https://www.mkdocs.org/user-guide/installation/) is a fast and simple **static site generator** that we use to run this Wiki. Install MKDocs using pip:

```
pip install mkdocs
```

Run `mkdocs --version` to make sure everything installed OK. If you are using Windows and the above command didn't work, try `python -m pip install mkdocs`.

We use the [Material](https://squidfunk.github.io/mkdocs-material/getting-started/) theme on top of MKDocs (makes site look nice). Run the following to install:

```
pip install mkdocs-material
```

This will automatically install compatible versions of all dependencies: MkDocs, Markdown, Pygments and Python Markdown Extensions.

## Formatting

We use Markdown for all files in the Wiki. Markdown is easy-to-use FOSS markup language you can use to format virtually any document. See the [Markdown Guide](https://www.markdownguide.org/) for more info on syntax.

## Make a New Page

If you want to get started with the Wiki, ask the admin to be added to the [GitHub repo for the wiki](https://github.com/uflautonomypark/apark-wiki). Once you are added to the repo, pull using

```
git clone https://github.com/uflautonomypark/apark-wiki.git
```

Navigate to the `\apark-wiki` directory and run `mkdocs serve`. Open up http://127.0.0.1:8000/ in your browser, and you'll see the Wiki home page being displayed.

To add a page to the Wiki, either create a folder (this will show up as a nav item in the sidebar) and add a `.md` file to the folder, or add a `.md` file to an existing directory.

Add a title block to your `.md` file:

```
---
title: Your Title Here
---
```

and you are off to the races.

We use relative paths for all files. If you want to add a PDF, keep it in the same directory as your Markdown file. Here is an example:

```
[Battery Manual](../../homebrew/tattu-manual.pdf)
```

We keep all images in the `\images` directory. Here is an example:

```
![Autonomy Park robots](images/robots.jpg)
```

To get your changes on the web, write a **detailed** commit message, and push your changes. I wrote a GitHub actions script that will automatically compile the site using `mkdocs`.
