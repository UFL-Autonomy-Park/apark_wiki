---
title: Minimal Startup
---

Author: Max Gardenswartz

The `https://github.com/UFL-Autonomy-Park/bebop_ws` repo contains all of the necessary packages for a minimal startup, joy control, and setpoint control for the Parrot Bebop 2 drones in the NCR lab. To build all packages and install the ROS2 driver for the Bebop, follow the instructions in the README.mds. Make sure to read all submodules README.mds.

DO NOT FORGET TO CORRECTLY ROTATE THE BEBOP's FRAME IN THE MOCAP SOFTWARE.

Our code assumes the mocap gives FLU. YOU MUST place the bebop at the origin of the lab (marked on floor), nose aligned with the positive x axis, and setup the frame to be FLU in OptiTrack.

In Optitrack, red is x, green is y, and blue is z.

This Bebop_ws does not contain example code for offboard control. It's the just the suite that's ready to accept velocity-level commands.

Here's some example code:

https://github.com/UFL-Autonomy-Park/bebop-rise-controller

Use the main.launch.py file. All params needed for bebop_ws are here. This launch file launches the example code AND the bebop_ws.

Take the quadoff. "Start" on the XBOX 360 controller. Land is the adjacent one. "A" to enter/exit offboard and start running code.
