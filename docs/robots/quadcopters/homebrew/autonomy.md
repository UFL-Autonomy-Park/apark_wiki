---
title: Autonomy
author: "Max Gardenswartz"
updated: 2026-11-10
applies_to: [apark]
assisted_by: Claude
glance: >-
  A Docker container that runs MAVROS and the ZED ROS 2 wrapper on any Homebrew. Use it instead of installing them by hand.
---

Everything on this page runs on Linux.

--8<-- "rtk-first.md"

[RTK Setup](../../../hardware/rtk-setup.md){ .md-button }

--8<-- "good-fix-quadcopter.md"

We have developed a Docker container which allows you to run MAVROS and the Zed ROS2 Wrapper quickly and easily on any of the Homebrew drones. 

We are using a slightly modified version of the Docker image found in the [zed-ros2-wrapper](https://github.com/UFL-Autonomy-Park/zed_ros2_wrapper_jetson#). For a full install guide, see the README in the [homebrew_docker](https://github.com/UFL-Autonomy-Park/homebrew_docker) repository. 