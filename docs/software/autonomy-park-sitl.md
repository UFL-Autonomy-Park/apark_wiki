---
title: Autonomy Park SITL
author: Max Gardenswartz
updated: 2026-11-06
status: draft
status_note: Still in development. The first release is expected in December 2026.
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  The Autonomy Park SITL is a simulation environment for testing robot-ready code. It is in development; a release for one quadcopter is expected in December 2026.
---

A SITL (software in the loop) is a simulation environment for testing robot-ready code before it runs on a real robot. The setup instructions, the commands, and the supported versions are in the repository's README.

!!! note "The Repository Is Private"
    The Autonomy Park SITL repository is private. To see it, get access on [GitHub Access](../start-here/access/github-access.md).

[Autonomy Park SITL](https://github.com/UFL-Autonomy-Park/autonomy_park_sitl){ .md-button }

## Status

It is still in development.

* **Quadcopters:** it supports one Homebrew or one generic quadcopter. Multi-agent simulation is not supported. A release for this is expected in December 2026.
* **Unitree quadrupeds, and ground robots such as the Husky A200 and the Jackal UGV:** simulation is in development, and is expected in March 2027.

Anyone using the Astros or Homebrews for offboard control must simulate in the SITL first: see [Lab Rules](../start-here/lab-rules.md).