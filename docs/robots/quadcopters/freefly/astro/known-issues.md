---
title: Known Issues
author: Max Gardenswartz
updated: 2026-11-10
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  The Astros are great for most work, but not for offboard controls research. Their remotes drain fast, and a repair takes a year or more.
---

!!! danger "The Herelink Remotes Drain Very Quickly"
    The Astros' Herelink RC controllers drain their batteries very quickly. You still need one to fly or land safely when using offboard control. Charge it before every flight and watch its battery.

!!! danger "Never Update the Herelink Controllers"
    Do not update the software or the AMC version on the Herelink controllers. A newer version installed by mistake on astro2's remote caused a poor radio connection, apps that no longer work, and parameters with new limits, and it has not been fixed.

## Not Recommended for Offboard Controls Research

Do not use the Astros for offboard controls research (for example, an adaptive control paper), because:

1. The onboard computer is weak.
2. The telemetry rate cannot be raised above the default 30 Hz.
3. The Chrony server cannot be used to monitor the health or age of the telemetry and the PX4 link.

The Astros are great for everything else. For controls experiments, use a Homebrew.

## Repairs Are Slow and Expensive

The Astros are much more expensive to break than the Homebrews. Sending one to Freefly for repair takes about a year or more. See [Repairs](../repairs.md).
