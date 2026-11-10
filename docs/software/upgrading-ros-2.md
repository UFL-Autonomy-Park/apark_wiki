---
title: Upgrading ROS 2
author: "Max Gardenswartz"
updated: 2026-11-10
assisted_by: Claude
applies_to: [apark, indoor-lab]
glance: >-
  Why a ROS 2 upgrade is a months-long project, and how to find everything that must be checked first. Read it before you plan one.
---

!!! danger "Do Not Take a ROS 2 Upgrade Lightly"
    Updating ROS 2 requires upgrading every computer, every Docker container, and most of the robots. This will take months or over a year to do, test, and debug.

ROS 2 is released in lockstep with Ubuntu LTS versions: each ROS 2 long-term release is built for one Ubuntu LTS release, so a new ROS 2 distribution means a new Ubuntu on the computers too. The list of distributions and their end-of-life dates is on the [ROS 2 releases page](https://docs.ros.org/en/rolling/Releases.html#list-of-distributions).

## Where We Are

ROS 2 Humble is scheduled to reach end of life in 2027. We will likely switch to the latest stable ROS 2 distribution after this. Since this requires massive effort, we will delay it as long as possible, though.

!!! danger "Approval Needed"
    Dr. Kamalapurkar owns all robots and thus approves major upgrades like these.

## Finding What an Upgrade Touches

[Software We Use](software-we-use.md) was made to help you check all of the many places whose compatibility with a ROS 2 upgrade must be checked, or reworked from scratch, before an upgrade.
