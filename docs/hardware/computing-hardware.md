---
title: Computing Hardware
author: "Brandon Fallin, Max Gardenswartz"
updated: 2026-11-06
applies_to: [apark]
assisted_by: Claude
glance: >-
  The specifications and roles of the Autonomy Park's computers and the NAS. Look here to pick the right machine for a job.
---

| Computer | Role | CPU | GPU | RAM | Storage | Last Updated |
|---|---|---|---|---|---|---|
| Observer | Observes experiments, collects data, and (in theory) displays data on the 6 monitors in the Command Shed | Intel i9-12900KS | NVIDIA RTX 4070 Ti | 32 GB | 5 TB | 2026-10-21 |
| Atlas | Handles demanding computational tasks and simulations | AMD Ryzen Threadripper Pro 3975WX | 2x NVIDIA RTX 3080 Ti | 512 GB | 10 TB | 2026-10-21 |
| Superman | The heart of the Autonomy Park: the main computer in the Command Shed that runs the 6 monitors. This is typically where you launch ROS nodes from | Intel i9-9820X | 2x NVIDIA RTX 2080 Ti | 128 GB | 1 TB | 2026-10-21 |
| Steve | Located in NEB 405. Used mainly for Gazebo simulations | Intel i9-11900K | NVIDIA RTX 3090 Ti | 128 GB | 2 TB | 2026-10-21 |
| NAS | Where we keep all of our data. Runs TrueNAS Scale | 2x Intel Xeon E5-2697 | None | 128 GB | 192 TB | 2026-10-21 |
