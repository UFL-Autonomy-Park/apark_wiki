---
title: Upgrading PX4 Firmware
author: Max Gardenswartz
updated: 2026-10-22
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  Upgrading PX4 on a Homebrew is expert work. PX4 has no tool to port parameters between versions, so the template must be ported by hand and tested on one quadcopter first.
---

!!! warning "Updating PX4 Needs Serious Expertise"
    Do not upgrade PX4 on a quadcopter you plan to fly soon. Do it on a single quadcopter, as described below.

[Case Study: Porting the Homebrew Parameters to PX4 Main](../case-studies/porting-the-parameters-to-px4-main.md){ .md-button }
[What Is Safe to Upgrade](../../../../software/what-is-safe-to-upgrade.md){ .md-button }

!!! note "Upgrading May Get Easier"
    PX4 pull request [#29363](https://github.com/PX4/PX4-Autopilot/pull/29363) introduces safe parameter migration from 1.17 to the 1.18 beta. Upgrading may be easier someday. For now, manual porting is the only safe way to upgrade from 1.16 to future versions.

## Why Upgrading Is Manual

PX4 does not provide a porting tool for parameters between versions. Major (1.x to 2.x) and minor (x.15 to x.16) updates often involve opaque changes to parameter names and EKF logic.

* **Standard Practice:** Users are expected to reconfigure PX4 from scratch when a new minor/major version is released.
* **Legacy Data:** If you update firmware from a previous version, PX4 will attempt to keep as many parameters as possible. This is **undesirable** and leads to errors.
* **Deltas:** The comparison script, [px4-param-diff.py](../px4-param-diff.py){ download="px4-param-diff.py" }, was used to identify differences between a working 1.15.4 set and a default 1.16.0 set to create our current template. Use it as a baseline for future upgrades (e.g., 1.16 to 1.17).

## Procedure

1. Port the parameter template by hand. Go through [Homebrew Parameters](../parameters.md) one parameter at a time against the parameter reference of the new PX4 version, and update the template for that version.

2. Update PX4 on a **single** quadcopter.

3. On that quadcopter, follow steps 2 to 9 of the [Clean Configuration Procedure](../px4-configuration.md#clean-configuration-procedure), then the battery voltage calibration in [PX4 Configuration](../px4-configuration.md#battery-voltage-calibration).

## Verifying the Upgrade

The biggest check is the parameter names: make sure every setting you want was ported to its new parameter name. (PX4 1.15.0 to 1.16.0 was a nightmare for this.) Stability of flight is not the main check.

Then fly. Do multiple manual test flights of about 60 seconds each, in Position Mode. Include at least one cold restart, by unplugging and re-plugging the battery.

Something is wrong if the quadcopter drifts in Position Mode with the sticks centered (see [Position Mode Should Hold Position](../flying-manually.md#position-mode-should-hold-position)), if `fix_type` is ever less than 6, if flying feels off, or if the quadcopter crashes unexpectedly.

--8<-- "good-fix-quadcopter.md"

!!! warning "Position Mode Is Already Quite Fast"
    Be very careful. Move the sticks very slowly.

!!! danger "Never Upgrade the Fleet Before Test Flights on One Quadcopter"
    Upgrading the rest of the fleet without test flights on a single upgraded quadcopter first is a bad idea.

## Updating the Rest of the Fleet

Only after the single quadcopter passes its test flights, the person upgrading the fleet needs to:

1. **Save the firmware.** Download the firmware for the CubePilot Orange from QGC's Firmware tab and save it to the wiki (see [PX4 Configuration](../px4-configuration.md#firmware-management)). It takes some digging to find the downloaded file. The exact steps: *Not yet documented*{ .unknown }.
2. **Update the references.** Update the [Homebrew Parameters](../parameters.md) reference and the [Calibration Parameters](../calibration-and-per-drone-parameters.md) page, which are detailed on the [PX4 Configuration](../px4-configuration.md) page.
3. **Generate a new `.params` file** like the current one in the parameter template. Do **not** generate it from a full parameter set saved from a working upgraded quadcopter: that set contains its calibration values.
4. **Apply the procedure** in the [Clean Configuration Procedure](../px4-configuration.md#clean-configuration-procedure) to every quadcopter.

!!! info "When You Do Not Need to Wipe Parameters and Recalibrate"
    The Clean Configuration Procedure wipes all previous parameters (Reset all to firmware's defaults) and has every sensor recalibrated. You can avoid both if you verify that **none** of the calibration parameter names in [Calibration Parameters](../calibration-and-per-drone-parameters.md) changed in the new PX4 version.

    If only some sensors had their calibration parameter names changed, a full reset is also not needed: recalibrate only those sensors.

    If you cannot verify the names, the Clean Configuration Procedure must be followed in full for every quadcopter.

    In that case, battery recalibration can also be skipped, because `BAT1_V_DIV` and `BAT1_A_PER_V` are calibration parameters too. Load the revised `.params` file (the same set of parameters, with updated names), reboot, and fly.

!!! note "QGC May Show a \"Missing Parameters\" Message"
    After a firmware update, QGC may show a "Missing parameters" message. It can generally be ignored. It is common when updating firmware.
