---
title: Security Cameras
author: Max Gardenswartz
updated: 2026-11-03
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  The Autonomy Park cameras record to a Lorex NVR that keeps only the last 24 hours. Getting good footage out of it is very difficult.
---

!!! warning "Do Not Count on the Footage"
    The cameras record to a Lorex NVR. It is very difficult to get good footage from them.

* **Where:** the NVR is at `192.168.1.33`. You can also reach it with the Home Assistant bookmark in the Chrome browser on the Autonomy Park computer.
* **How long:** only the last 24 hours are stored.
* **Replay:** replaying footage on the NVR works, but it can skip around unexpectedly.
* **Quality:** the video quality is poor.
* **Getting files out:** pulling files directly onto a USB stick is nearly impossible.

The other Autonomy Park addresses are on [IP Reservations](../software/ip-reservations.md).
