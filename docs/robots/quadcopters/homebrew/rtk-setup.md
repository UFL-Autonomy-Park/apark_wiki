---
title: RTK Setup
author: Max Gardenswartz
updated: 2026-11-10
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  A Homebrew gets RTK corrections automatically once the ground station is on, homebrew_docker is set up, and the parameters are set.
---

--8<-- "rtk-intro.md"

!!! warning "Start the Homebrew Outdoors"
    Start the Homebrew outdoors, never indoors.

Follow these in order. After them, RTK works.

1. Watch the [Homebrew setup video](overview.md#setup-video).
2. Follow the instructions in [homebrew_docker](https://github.com/UFL-Autonomy-Park/homebrew_docker). It contains the NTRIP client that takes corrections from the RTKLib caster. Use the RTKLib caster, never the RS3's embedded caster.
3. Follow [RTK Setup](../../../hardware/rtk-setup.md) so the ground station is on.
4. Check that the parameters are set as described in [PX4 Configuration](px4-configuration.md).

To see whether each Homebrew has `homebrew_docker` set up, see the table [Status of Each Homebrew](known-issues.md#status-of-each-homebrew).
