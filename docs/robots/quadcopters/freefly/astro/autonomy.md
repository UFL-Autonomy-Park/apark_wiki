---
title: Autonomy
author: "Max Gardenswartz, Brandon Fallin"
updated: 2026-11-10
applies_to: [apark]
assisted_by: Claude
glance: >-
  How offboard control works on the Astros and its limits: the astro_mavros app, no SSH, no torque-level control.
---

[Flying Manually](operate/flying-manually.md#tutorial-video) has a tutorial video on flying the Astros and using autonomy with them.

MAVROS is needed for off-board control or teleoperation. See our [astro_mavros](https://github.com/UFL-Autonomy-Park/astro_mavros) app on GitHub.

!!! warning "Torque-Level Offboard Control Is Not Possible"
    On 2026-10-20 Freefly support confirmed that the Astros do not support the Micro XRCE-DDS Agent for offboard control, so torque-level control is not possible on them. Freefly has no plans to support it, even though AuterionOS does. Only Freefly can enable or disable it.

!!! note "No SSH, and the App API Version"
    Only version 4 and newer of the Freefly app API allow SSH. Our stack, [astro_mavros](https://github.com/UFL-Autonomy-Park/astro_mavros), uses version 1, so you cannot SSH into the Astros. Future Freefly releases may deprecate version 1. Freefly supports up to version 4, which would allow SSH, but this has not been tested. AuterionOS itself is at version 7 ([App Framework](https://docs.auterion.com/app-development/app-framework/app-framework-1)), which Freefly does not support.

!!! note "Topics Do Not Cross-Publish, but More Test Flights Are Needed"
    Freefly forces `MAV_SYS_ID`, which could make topics cross-publish into each other. `astro_mavros` is written to avoid this. More test flights are needed to be sure.

!!! note "Software Versions"
    `astro_mavros` is tested with MAVROS 2.16.0 alongside the latest Freefly software. Astros running software older than 2.2.6 could no longer connect to the internet to serve topics, so they had to be updated.

## Which Astros Work

| Astro | `astro_mavros` |
|---|---|
| astro1 | Works off the shelf |
| astro2 | Works off the shelf |
| astro3 | Not set up |

## Controls Experiments

!!! warning "The Astros Are Not Good for Controls Experiments"
    The MAVROS pose rate of the Astros is 30 Hz and cannot be raised. (On the Homebrews it can.) The latency between the companion computer and PX4 is also rather high, and the Astros do not support uXRCE-DDS (see above). Use a Homebrew for controls experiments.
