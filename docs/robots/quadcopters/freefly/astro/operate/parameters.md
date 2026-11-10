---
title: Parameters
author: "Brandon Fallin, Max Gardenswartz"
updated: 2026-11-10
applies_to: [apark]
assisted_by: Claude
glance: >-
  The parameters to set on every Astro, and which are critical for safety. The PX4 wiki is not a reliable guide for them.
---

!!! warning "Check These Settings Before Every Flight"
    Before you take off the Astro, make sure the parameters in the table below are set as listed. In the **Safety** settings, also make sure that all RTL and takeoff altitudes are not greater than 2.5 m.

!!! danger "The PX4 Wiki Is Not an Accurate Guide for These Parameters"
    The Astros run an out-of-tree version of Auterion PX4 (APX4), which is itself a branch of PX4. Software stack v2.3.7 uses APX4 3.2.8 (`v1.15.0-3.2.8-558-g98feccfbd6`). Parameter names, ranges, and behavior can differ from the PX4 wiki. Trust this page, not the PX4 wiki.

## How to Change Parameters

There are three ways.

1. **Auterion Mission Control (AMC) on your computer.** Download AMC from Auterion Suite. It is free, but you need to log in.
2. **The USB-C port.** Connect to the Astro's [USB-C port](../usb-c-port.md) and set the parameters in the dashboard at `https://10.41.1.1/`. This is the equivalent of QGroundControl on the Homebrews.
3. **AMC on the Herelink controller.** Tap the navigation arrow (menu) in the top left 7 times, then tap **Switch to Advanced Mode**. **Parameters** is then available under **Advanced** in the menu.

## Parameters to Set

Set every Astro to the values in the **Set To** column. astro1 and astro2 were checked on software v2.3.7. astro3 has not been checked.

| Parameter | Set To | Notes |
|---|---|---|
| `BAT_CRIT_THR` | 0.4 | |
| `BAT_EMERGEN_THR` | 0.3 | |
| `COM_LOW_BAT_ACT` | 3 (Land mode) | **Critical.** |
| `COM_ARM_GCS_REQ` | 1 (Enabled) | Stops offboard programs from arming without the RC. Otherwise this is a safety issue. |
| `COM_RC_OVERRIDE` | 3 | Needed so the RC can override offboard code and auto modes. |
| `NAV_RCL_ACT` | 3 (Land mode) | |
| `EKF2_GPS_CTRL` | 7 | Needed so the altitude estimate uses the RTK values, and so it is consistent across reboots with the code in `aero_common`. Otherwise the z-estimate is all over the place. This is not dangerous only because we use RTK. |
| `RTL_RETURN_ALT` | 2 | **Critical.** Meters. |
| `RTL_DESCEND_ALT` | 2 | **Critical.** Meters. |
| `COM_FLTMODE5` | 9 (Position Slow) | Does not really matter. |
| `COM_GCS_SYS_ID` | *Unknown*{ .unknown } | |
| `FF_INPUT_TYPE` | 6 | |
| `MC_SLOW_MAP_HVEL` | 0 | Effect unknown. |
| `MC_SLOW_MAP_VVEL` | 0 | Effect unknown. |
| `MC_SLOW_MAP_YAWR` | 0 | Effect unknown. |
| `RC_MAP_AUX1` to `RC_MAP_AUX4` | 0 | Effect unknown. |
| `RC11_MAX` to `RC16_MAX` | 2000 | |
| `RC11_MIN` to `RC16_MIN` | 1000 | |
| `RC11_TRIM` to `RC16_TRIM` | 1500 | |
| `EKF2_RNG_CTRL` | 1 (Enabled conditionally) | Left at Freefly's default; helps with landing, but RTK makes it somewhat unnecessary. |
| `COM_OBL_RC_ACT` | Position Mode | Drops you into Position Mode (thus holding in place) if the off-board heartbeat stops for `COM_OF_LOSS_T` seconds. |
| `TC_*` | Do not change | Sensor calibration values, individual to each quadcopter. |

!!! note "Some Raw Values Are Missing"
    Max could not determine the raw value of every parameter above.

## Freefly's Recommended Parameters

Unlike upgrading PX4 on the Homebrews, flashing a new Freefly Astro software bundle (and so a new AuterionOS) gives you the set of parameters Freefly recommends. Stick to these, apart from the parameters in the table above. Freefly does not port your own parameters when you upgrade either, so write down any you change.
