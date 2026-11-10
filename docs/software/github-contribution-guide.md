---
title: GitHub Contribution Guide
author: "Max Gardenswartz"
updated: 2026-11-10
assisted_by: Claude
applies_to: [apark, indoor-lab]
glance: >-
  How to commit, branch, review, tag, and archive code in our GitHub organization, and when a repository is public or private. Read it before you push.
---

Our code lives in the [UFL-Autonomy-Park](https://github.com/UFL-Autonomy-Park/) GitHub organization. To get access to the private repositories, see [GitHub Access](../start-here/access/github-access.md).

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/). Start each commit message with a type, then a short description:

```text
feat: add a landing-pad detector
fix: stop the node from crashing when the lidar drops out
docs: explain how to calibrate the camera
```

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, and `chore`. Keep each commit to one change.

## Branches and Pull Requests

- Develop every feature on its own branch. Do not commit features straight to `main`.
- Open a pull request when the feature is tested and ready for development, meaning it is ready for the rest of us to build on.
- Test before you open the pull request, and say in it how you tested.

## Version Tags

Tag each release with a version number, such as `v1.2.0`, so anyone can return to the exact code behind an experiment.

## Archiving Old Code

When a repository is no longer maintained, archive it on GitHub instead of deleting it. Archived code stays readable, and the history of past papers and projects is kept.

## The README

Every README must say which paper or project the repository is for.

## Public and Private

- Keep shared code public.
- Keep anything that will go in a paper private until it is published.
- **Never change a repository between public and private without asking first.** Ask a person on the [Contacts](../start-here/contacts.md) page.
