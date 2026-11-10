---
title: What Is Safe to Upgrade
author: Max Gardenswartz
updated: 2026-11-06
status: active
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  Which software and firmware you can upgrade without breaking our code, and which need serious expertise. When in doubt, do not upgrade.
---

**Safe** here means reasonably safe: nothing will break if you use the same code, and no documentation will need to change. Anything marked as needing testing must be tested on a single robot first.

| Component | Safe to Upgrade? | Notes |
|---|---|---|
| Emlid receiver firmware | ✅ Safe | |
| Emlid Flow app | ✅ Safe | |
| QGroundControl | ✅ Safe | |
| Here4 firmware | ✅ Safe | |
| Auterion CLI | ✅ Safe | |
| Minor `apt` upgrades | ✅ Safe | A minor `apt` upgrade may also update MAVROS, which is not safe. |
| MAVROS | ❌ Not safe | Needs testing. |
| Docker | ⚠️ Sometimes | Some upgrades (such as `apt` upgrades) are safe, others are not. Needs testing. |
| PX4 | ❌ Not safe | Port the parameters by hand: see [Upgrading PX4 Firmware](../robots/quadcopters/homebrew/maintain/upgrading-px4-firmware.md). |
| JetPack | ❌ Not safe | Needs a revised `homebrew_docker`. |
| ROS 2 distribution | ❌ Never | |
| Ubuntu version | ❌ Never | See [Software We Use](software-we-use.md#ubuntu). |
| OptiTrack Motive | ❌ Cannot be upgraded | Our license, and so our access to updates, expired. If the license key is lost, or Motive stops working (for example after a forced Windows upgrade), replacing it is not safe: it would force a switch from VRPN to NatNet. |
| Freefly Astro software | ⚠️ Sometimes | It depends on if Freefly updates the minor version of the underlying APX4. All updates tested thus far have not changed the PX4 version and have been fine. |

## Planned Changes

These are optional and not urgent. Whoever wants to spend the time, and the need for it, decides when.

* **MAVROS to uXRCE-DDS for the Homebrews,** after PX4 1.19.0 is released. PX4 1.19.0 is a long way off. See the [Case Study: Porting the Homebrew Parameters to PX4 Main](../robots/quadcopters/homebrew/case-studies/porting-the-parameters-to-px4-main.md).
    * `homebrew_docker` contains [aero_common](https://github.com/UFL-Autonomy-Park/aero_common), which makes offboard programs more modular. `aero_common` will need updates for the switch. Once they are tested in the [Autonomy Park SITL](autonomy-park-sitl.md), it should pretty much work.
    * One caveat: the MicroStrain `ntrip_client` in `homebrew_docker` uses MAVROS. Using XRCE (a brand-new feature) needs code Max wrote in the `rtk_tests_for_px4_1_18` branch of `homebrew_docker`, which would have to be merged into `main`.
