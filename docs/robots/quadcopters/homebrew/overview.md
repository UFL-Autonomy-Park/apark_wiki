---
title: Overview
author: "Brandon Fallin, Max Gardenswartz"
updated: 2026-11-10
assisted_by: Claude
applies_to: [apark]
glance: >-
  Quick facts about the Homebrew: physical measurements, manuals, and video guides. Look here when you need a number or a manual.
---

![A Homebrew quadcopter on a wooden floor, seen from behind, with a black carbon-pattern canopy, a GPS puck on a short mast, and four arms with motors.](../../../images/homebrew/homebrew.jpg){ width="40%" }

*A Homebrew.*

[Bill of Materials](https://drive.google.com/drive/folders/1Uk_7wlghpHyelc945v2afTTQlUkaxDso?usp=sharing){ .md-button }

--8<-- "rtk-first.md"

[RTK Setup](../../../hardware/rtk-setup.md){ .md-button }

--8<-- "rtk-fix-danger.md"

--8<-- "flight-modes-danger.md"

--8<-- "lidar-flow-clearance.md"

--8<-- "battery-watch-danger.md"

--8<-- "lidar-wiring-danger.md"

!!! warning "Attaching a Payload"
    Disable `EKF2_OF_CTRL` and `EKF2_RNG_CTRL` if you attach a payload. Move slowly. Do not attach more than 1 kg: this is the tested safe limit.

    For controls experiments, consider also disabling `MPC_USE_HTE` and manually tuning `MPC_THR_HOVER` (not to exceed 0.7). See [Parameters](parameters.md).

## Pages

| Page | What it covers |
|---|---|
| [Known Issues](known-issues.md) | Read before you fly: problems, and the status of each Homebrew |
| [Batteries](batteries.md) | The 6S LiPo packs and how to track their age |
| [RTK Setup](rtk-setup.md) | How a Homebrew gets RTK corrections |
| [PX4 Configuration](px4-configuration.md) | The steps to configure a Homebrew and calibrate it on its own |
| [Parameters](parameters.md) | Every PX4 parameter the Homebrew template sets, and why |
| [Calibration and Per-Drone Parameters](calibration-and-per-drone-parameters.md) | The parameters that are unique to each Homebrew and never copied |
| [Microhard Radios](microhard-radios.md) | The planned data link for multi-agent flights |
| [Flying Manually](flying-manually.md) | Flying a Homebrew by hand: pre-flight, takeoff, landing |
| [Autonomy](autonomy.md) | A Docker container that runs MAVROS and the ZED ROS 2 wrapper |
| [Build](build/overview.md) | How the Homebrews were built (kept as reference) |
| [Maintain](maintain/service-and-repair-manual.md) | Repair, PX4 firmware upgrades, building PX4, and Here4 firmware |
| [Case Studies](case-studies/porting-the-parameters-to-px4-main.md) | What went wrong, and what we learned |
| [Jetsons](../../../hardware/jetsons.md) | Using and flashing the Jetsons (in Hardware) |
| [Radio and RC Setup Guide](../../../hardware/radio-and-rc-setup-guide.md) | The legacy FrSky radio setup (in Hardware) |

## Setup Video

A video on setting up the Jetson, what to look for, and a general orientation to the RC and QGroundControl radio setups:

<iframe width="560" height="315" src="https://www.youtube.com/embed/Wczulgm0QgA" title="Homebrew setup video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

!!! note
    It is okay to cut the case to make room for cables.

## Manuals

[Battery Manual](tattu-manual.pdf){ .md-button }

[LIDAR Manual](lidar-manual.pdf){ .md-button }

[Here 4 GPS Manual](https://docs.cubepilot.org/user-guides/here-4/here-4-manual){ .md-button }

## Video Guides

[RFD900x Wiring](https://www.youtube.com/watch?v=UBxZTWxYdXM){ .md-button }