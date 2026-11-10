---
title: "Case Study: MAVROS Link Saturation"
author: Max Gardenswartz
updated: 2026-11-10
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  On 2026-10-09, Homebrew 03 flew into the net because MAVROS saturated the serial link to the flight controller and offboard control acted on old state data. Read this before you run offboard code of any kind on a Homebrew.
---

## What Happened

On 2026-10-09, Homebrew 03 crashed into the net. The same drone, parameters, and code had worked on 2026-10-07.

The round-trip time (RTT) on the data link between the Jetson and the flight controller was 2500 ms. Offboard control therefore acted on old state data. It believed the quadcopter was stuck on the ground, and did exactly what it should do in that case with that data: it launched the quadcopter into the net. Nothing in the offboard control code Max wrote was monitoring for this kind of failure.

The drone took off as part of an offboard program for Max's research. Instead of climbing normally, it launched itself straight upward into the net.

<figure markdown="span">
  <video src="../../../../../videos/homebrew-03-crash-2026-10-09.mp4" autoplay loop muted playsinline controls width="100%"></video>
  <figcaption>Homebrew 03 crash, 2026-10-09: the offboard takeoff launches the drone straight up into the net.</figcaption>
</figure>

## Why

The serial link out of PX4 carries only 40 to 64 KB/s. With all the MAVROS plugins on (which is the default, shockingly!) MAVROS requested so much data that the link saturated. PX4 never cleared the backlog of requests from MAVROS, so everything it sent back was late.

## What to Do

* Do not run MAVROS with every plugin enabled on a Homebrew. The latest version of [homebrew_docker](https://github.com/UFL-Autonomy-Park/homebrew_docker) has the fixes to use fewer plugins. It also has the list of plugins deemed necessary for basic offboard functionality and safety checks.
* Monitor the link while the offboard program runs. The example code in [autonomy_park_sitl](https://github.com/UFL-Autonomy-Park/autonomy_park_sitl) has a comprehensive set of tests needed to safely monitor this connection (and many other things) so the offboard program acts in a safe manner.
* Control barrier functions for offboard control do not exist yet. They still need to be written, as of writing this.

[homebrew_docker](https://github.com/UFL-Autonomy-Park/homebrew_docker){ .md-button }
[autonomy_park_sitl](https://github.com/UFL-Autonomy-Park/autonomy_park_sitl){ .md-button }

## Related

* The Homebrew 02 flight controller has slow XRCE topics (94 Hz); the cause is unknown. See [Known Issues](../known-issues.md#status-of-each-homebrew).
* [Case Study: Lidar and CAN Sensor Burnout](lidar-and-can-sensor-burnout.md): the lidar and optical flow on this drone had also failed before the crash.
