---
title: Example Parameters for PX4 Main
author: Max Gardenswartz
updated: 2026-10-22
status: draft
status_note: An example for the case study only. Valid only for PX4 main at commit 5f429033bf and the PR 29368 branch on 2026-10-22.
applies_to: [apark]
assisted_by: Claude
glance: >-
  The parameter reference produced by the porting case study. It is an example of the result, not a template to load on a real Homebrew.
---

!!! danger "Example Only: Do Not Load These on a Homebrew"
    These parameters were made for PX4 `main` at commit `5f429033bf` and the open PR #29368 branch, tested on 2026-10-22. Loading them on 1.16.2 or on any stable release can set parameters that do not exist, or that mean something different. The parameters to use on the fleet are in [Parameters](../parameters.md).

    The matching file is [example-parameters-px4-main.params](example-parameters-px4-main.params). It is also an example only. The method is in [Case Study: Porting the Homebrew Parameters to PX4 Main](porting-the-parameters-to-px4-main.md).

Reference: PX4 **main** at commit `5f429033bf` (2026-10-22, the 1.19 development line), with the open pull request [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368) (RTCM corrections over uXRCE-DDS) as the branch under test. This is the main-line port of the v1.16.2 version of this document; [the case study](porting-the-parameters-to-px4-main.md) shows how it was made. "Default" means the main metadata default **plus** the CubePilot Cube Orange board defaults (`rc.board_defaults`), the multicopter defaults in `rc.mc_defaults` (which overrides `RTL_RETURN_ALT` and `RTL_DESCEND_ALT` and sets `MAV_TYPE`), and the Generic Quadcopter airframe defaults (`4001_quad_x`, which sets the `CA_ROTOR*` positions). None of those layered defaults changed from 1.16.2 for the parameters in this document.

!!! warning
    **Do not use this for porting to 1.18.0 or any other stable release.** Main differs from release/1.18 (for example `GNSS_CHECK`, `GNSS_REQ_*` and `SENS_GNSS0_*` exist only on main; release/1.18 still has `EKF2_GPS_CHECK`, `EKF2_REQ_*` and `SENS_GPS0_*`). Regenerate this document against the target release.

Legend: ✅ = matches the multicopter default, ❌ = differs from the multicopter default.

## BAT: Battery

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `BAT1_CAPACITY` | -1 | Disabled | ✅ | Default −1 (unknown). Left disabled so remaining charge is estimated from voltage only. The current sensor is not working, so coulomb counting would integrate invalid current. Set to 16000 mAh (all Homebrew batteries) once current sensing is verified. |
| `BAT1_I_OVERWRITE` | 0 A | Idle-current overwrite disabled | ✅ | Default 0 (disabled, the measured current is used). |
| `BAT1_N_CELLS` | 6 | 6S battery | ❌ | Default 0 (unknown). Should be set by the user to match the battery. |
| `BAT1_R_INTERNAL` | −1 Ω | Use the online estimate | ✅ | Default −1 (use the online estimate). Left at default because the current sensor is not working, and both the sag compensation and the online estimate need valid current. The PX4 parameter description says this is *per cell*. |
| `BAT1_SOURCE` | 0 | Battery 1 read from the power module | ✅ | Default 0 (labelled "Power Module / Analog" on main, "Power Module" in 1.16.2). The other options are 1 (External, from MAVLink battery status messages) and 2 (ESCs, taken from the `esc_status` message, which per the v1.16.2 description requires the ESCs to report both voltage and current). PX4 currently cannot read the current from the PDB. Max thinks setting this to 2 might fix that, but this is not verified, and since the notes for `COM_ARM_CHK_ESCS` say these ESCs do not support telemetry, it may not be possible at all. Requires reboot. |
| `BAT1_V_CHARGED` | 4.2 V | 4.2 V per cell when full | ✅ | Default 4.2 V on main (4.05 V in 1.16.2). The old 4.05 V was a deliberate workaround: the voltage is read from a quadcopter drawing about 5 A, and battery sag makes a full 4.2 V cell read about 4.05 V. Main changed the default and dropped the 1.16.2 description's advice to set this below 4.2 V; Max decided to trust the new default. Remaining charge is a linear interpolation between `BAT1_V_EMPTY` and `BAT1_V_CHARGED` (`battery.cpp`), so at the same measured voltage the estimate is now lower and every threshold below triggers at a higher voltage (more conservative; see `BAT_LOW_THR`, `BAT_CRIT_THR`, `BAT_EMERGEN_THR`, `COM_ARM_BAT_MIN`). The value also sets the over-voltage "spike" fault threshold (cells × `BAT1_V_CHARGED` × 1.05) and the battery scale used by `MC_BAT_SCALE_EN` (default 0, not set here). |
| `BAT1_V_EMPTY` | 3.6 V | 3.6 V per cell when empty | ✅ | Default 3.6 V. The PX4 LiPo default, defined as the per-cell voltage under load when the pack is effectively empty. |
| `BAT2_A_PER_V` | 17 | Battery 2 current scale at board default | ✅ | Default 17 (Cube Orange board default). Leave at default since there is no BAT2. |
| `BAT2_CAPACITY` | −1 mAh | Battery 2 capacity unknown | ✅ | Default −1. Leave at default since there is no BAT2. |
| `BAT2_I_OVERWRITE` | 0 A | Idle-current overwrite disabled | ✅ | Default 0. Leave at default since there is no BAT2. |
| `BAT2_N_CELLS` | 0 | Cell count unknown | ✅ | Default 0. Leave at default since there is no BAT2. |
| `BAT2_R_INTERNAL` | −1 Ω | Use the online estimate | ✅ | Default −1. Leave at default since there is no BAT2. |
| `BAT2_SOURCE` | −1 | Battery 2 disabled | ✅ | Default −1 (Disabled). Leave at default since there is no BAT2. |
| `BAT2_V_CHANNEL` | −1 | Battery 2 voltage ADC channel at board default | ✅ | Default −1 (board default). Leave at default since there is no BAT2. |
| `BAT2_V_CHARGED` | 4.2 V | 4.2 V per cell when full | ✅ | Default 4.2 V (4.05 V in 1.16.2). Leave at default since there is no BAT2. |
| `BAT2_V_DIV` | 10.1 | Battery 2 voltage divider at board default | ✅ | Default 10.1 (Cube Orange board default). Leave at default since there is no BAT2. |
| `BAT2_V_EMPTY` | 3.6 V | 3.6 V per cell when empty | ✅ | Default 3.6 V. Leave at default since there is no BAT2. |
| `BAT3_CAPACITY` | −1 mAh | Battery 3 capacity unknown | ✅ | Default −1. Leave at default since there is no BAT3. |
| `BAT3_N_CELLS` | 0 | Cell count unknown | ✅ | Default 0. Leave at default since there is no BAT3. |
| `BAT3_R_INTERNAL` | −1 Ω | Use the online estimate | ✅ | Default −1. Leave at default since there is no BAT3. |
| `BAT3_SOURCE` | −1 | Battery 3 disabled | ✅ | Default −1 (Disabled). Leave at default since there is no BAT3. |
| `BAT3_V_CHARGED` | 4.2 V | 4.2 V per cell when full | ✅ | Default 4.2 V (4.05 V in 1.16.2). Leave at default since there is no BAT3. |
| `BAT3_V_EMPTY` | 3.6 V | 3.6 V per cell when empty | ✅ | Default 3.6 V. Leave at default since there is no BAT3. |
| `BAT_AVRG_CURRENT` | 15 A | 15 A expected in-flight current | ✅ | Default 15 A. Only used to initialize the in-flight average-current estimate, which feeds remaining-flight-time and RTL triggering. |
| `BAT_CRIT_THR` | 0.25 | Critical at 25% remaining | ❌ | Default 0.07. Triggers the critical-battery reaction (land) much earlier, so the Homebrew lands with a healthy reserve (about 3.75 V per cell with the linear 3.6–4.2 V mapping; 3.71 V in 1.16.2 with 4.05 V). Must stay below `BAT_LOW_THR` and above `BAT_EMERGEN_THR`. Units are normalized 0–1, not percent. |
| `BAT_EMERGEN_THR` | 0.15 | Emergency at 15% remaining | ❌ | Default 0.05. Immediate-landing level (about 3.69 V per cell with the linear 3.6–4.2 V mapping; 3.67 V in 1.16.2). Must stay below `BAT_CRIT_THR`. |
| `BAT_LOW_THR` | 0.35 | Low at 35% remaining | ❌ | Default 0.15. First warning level (about 3.81 V per cell with the linear 3.6–4.2 V mapping; 3.76 V in 1.16.2). Must stay above `BAT_CRIT_THR`. |
| `BAT_V_OFFS_CURR` | 0 | No current-sensor voltage offset | ✅ | Default 0. Offset in volts, as seen by the ADC input of the current sensor, subtracted before the battery current is computed from the voltage. It was in the 1.16.2 `.params` template but had no row in the 1.16.2 document and no reason was recorded; the value equals the default, so it is kept as is. |

Note that `BAT1_V_DIV` and `BAT1_A_PER_V` are calibrated separately for every quadcopter!

On main only batteries 1 and 2 have `BAT*_V_DIV`, `BAT*_A_PER_V` and `BAT*_V_CHANNEL`, so those do not exist for battery 3. `BAT*_I_CHANNEL` no longer exists for any battery, and `BAT*_I_OVERWRITE` now exists for all three (in 1.16.2 battery 3 had no `BAT3_I_OVERWRITE`).

## CA: Control Allocator

Positions are along the body X and Y axes, in metres, relative to the center of gravity. They describe the physical span of the airframe and are critical to the motor mixer and flight stability. The Generic Quadcopter airframe (`4001_quad_x`) sets them to ±1 m. The metadata default is 0.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `CA_ROTOR0_PX` | 0.25 m | Rotor 0 at +0.25 m on X | ❌ | Default 1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR0_PY` | 0.25 m | Rotor 0 at +0.25 m on Y | ❌ | Default 1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR1_PX` | −0.25 m | Rotor 1 at −0.25 m on X | ❌ | Default −1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR1_PY` | −0.25 m | Rotor 1 at −0.25 m on Y | ❌ | Default −1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR2_PX` | 0.25 m | Rotor 2 at +0.25 m on X | ❌ | Default 1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR2_PY` | −0.25 m | Rotor 2 at −0.25 m on Y | ❌ | Default −1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR3_PX` | −0.25 m | Rotor 3 at −0.25 m on X | ❌ | Default −1 m (airframe 4001). Physical span of the airframe. |
| `CA_ROTOR3_PY` | 0.25 m | Rotor 3 at +0.25 m on Y | ❌ | Default 1 m (airframe 4001). Physical span of the airframe. |

## COM: Commander

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `COM_ACT_FAIL_ACT` | 0 | Warning only on actuator failure | ✅ | Default 0 (warning only). The action taken when the failure detector reports a failed actuator (motor); the other options are 1 Hold, 2 Land, 3 Return, and 4 Terminate. It only matters if the actuator failure check is enabled and configured through `FD_ACT_EN` and the `MOTFAIL_*` parameters (see the FD and MOTFAIL sections). Max is unsure whether this should be changed to Land (2) since the current sensor is not working, but he uses 0 and it has been fine. |
| `COM_ARM_AUTH_MET` | 0 | One-step arming | ✅ | Default 0 (one arm: request authorization and arm as soon as it is received). The alternative is 1 (two-step arm: the first arm command requests authorization and the second arms if it is authorized). It is only used when `COM_ARM_AUTH_REQ` is on, so it has no effect here. |
| `COM_ARM_AUTH_REQ` | 0 | No arm authorization required | ✅ | Default 0 (disabled). No authorization is required to arm other than the arm switch. |
| `COM_ARM_BAT_MIN` | 0.50 | Refuse to arm below 50% battery | ❌ | Default −1 (uses `BAT_CRIT_THR`). Prevents permanently damaging the battery through negligence. 0.50 corresponds to about 3.90 V per cell with the 3.6–4.2 V mapping (3.83 V in 1.16.2), so arming now needs a slightly fuller pack. |
| `COM_ARM_CHK_ESCS` | 0 | ESC arming checks disabled | ✅ | Default 0 (disabled). Enables checks of the ESCs' online status and failures. It is specific to ESCs that report telemetry and must only be enabled if the ESCs support it; these ESCs do not. |
| `COM_ARM_HFLT_CHK` | 0 | Disabled; allow arming even if hardfault files are on the SD card | ❌ | Default 1 (enabled). On main the check also covers watchdog dump files. Enabling means a failed USB connection prevents all further arming until you delete the logs from SD (via the NuttX terminal or taking the SD card out). Super annoying. **Still needed on main as of 2026-10-22:** [PX4 issue #29346](https://github.com/PX4/PX4-Autopilot/issues/29346) (hardfault of the USB MAVLink task after arming following a USB unplug) is **open at the time of writing**, and Max reports it affects our board. The issue is filed against the Cube Orange+; its author says it is fixed on `main` by PRs #28185 and #28197, which was not verified here, so this stays 0 until a test confirms the problem is gone. Trade-off: with the check off the vehicle can arm after an accidental USB disconnect. |
| `COM_ARM_MAG_STR` | 1 | Deny arming on a magnetic disturbance | ❌ | Default 2 (warning only). Controls what happens when the estimator detects a strong magnetic disturbance, as checked according to `EKF2_MAG_CHECK`: 0 disabled, 1 deny arming, 2 warning only. Denying arming, not just warning, keeps a vehicle with a disturbed magnetometer on the ground. |
| `COM_ARM_WO_GPS` | 0 | Deny arming when the GNSS checks fail | ❌ | Default 1 ("Allow arming (with warning)"; called "Warning only" in 1.16.2). For an autonomous quadcopter, having no usable GPS should stop it from moving forward. These drones only ever fly outdoors. On main, 0 denies arming in all modes when a check enabled in `GNSS_CHECK` fails (reported as, for example, "Preflight: GPS fix too low"; `estimatorCheck.cpp`). The 1.16.2 text also said a global position estimate is required, which is why `EKF2_HGT_REF` must stay 1; that part was not re-checked on main. With `GNSS_CHECK` = 2047 and `GNSS_REQ_FIX` = 6 (see the GNSS section) arming is denied unless the receiver reports RTK fixed. |
| `COM_ARMABLE` | 1 | Arming allowed | ✅ | Default 1 (arming allowed). Set it to 0 to prevent arming entirely, for example for safety or maintenance reasons, so the vehicle cannot be used by accident. |
| `COM_DISARM_LAND` | 2.0 s | 2.0 s of successful landing detected | ✅ | Default 2.0 s. PX4 must detect that the vehicle is on the ground for this long before disarming the motors at the end of Land mode procedure. |
| `COM_DISARM_PRFLT` | 10 s | Disarm after 10 s without takeoff | ✅ | Default 10 s. If the vehicle is armed and has not taken off within this time, it disarms again (a negative value disables this). The user has 10 s to act after arming. |
| `COM_DL_LOSS_T` | 5 s | GCS connection counted as lost after 5 s | ❌ | Default 10 s. Tighter is better, and 10 s is too generous, especially for an autonomous quadcopter. Because `NAV_DLL_ACT` is set as 0 later, this value is **ignored**, but it's good to have.  |
| `COM_FAIL_ACT_T` | 5 s | Wait 5 s in Hold before a failsafe action | ✅ | Default 5 s. Before a failsafe action (Return, Land, or Hold) is executed, PX4 first waits this long in Hold mode so the user can realize something is wrong. During that time the pilot cannot take over with the stick override (`MAN_OVERRIDE_SPD`), although switching modes is still allowed; afterwards the configured action runs and the stick override works again. A value of 0 removes the delay. From the description it applies to the failsafes that are active here, such as RC loss (`NAV_RCL_ACT`) and offboard loss (`COM_OBL_RC_ACT`); the GCS-loss failsafe is disabled (`NAV_DLL_ACT` = 0), so it never starts this wait (my reading of the description; not tested). The stick-override part comes from the 1.16.2 description (`COM_RC_OVERRIDE`) and was not re-verified against the failsafe code on main, where the override is now `MAN_OVERRIDE_SPD`. |
| `COM_FLT_TIME_MAX` | −1 s | No maximum flight time | ✅ | Default −1 (disabled). When set, the vehicle aborts the current operation and returns to launch once the time since takeoff exceeds this value, with a warning every minute starting at 90 % of it. No maximum flight time is used; the battery thresholds limit the flight time instead. |
| `COM_FLTMODE1` | 2 | Slot 1: Position ("Position / Cruise" on main) | ❌ | Default −1 (unassigned). Necessary for using the Taranis QX7 remote specifically. With `RC_MAP_FLTMODE` the mode is picked by the range channel 5 is in, across six slots. **A different RC would need a different scheme.** |
| `COM_FLTMODE2` | 1 | Slot 2: Altitude | ❌ | Default −1 (unassigned). Same Taranis QX7 scheme. |
| `COM_FLTMODE3` | 4 | Slot 3: Hold | ❌ | Default −1 (unassigned). Same Taranis QX7 scheme. |
| `COM_FLTMODE4` | 1 | Slot 4: Altitude | ❌ | Default −1 (unassigned). Same Taranis QX7 scheme. Slots 2 and 4 are both Altitude. |
| `COM_FLTMODE5` | 11 | Slot 5: Land | ❌ | Default −1 (unassigned). Same Taranis QX7 scheme. |
| `COM_FLTMODE6` | 8 | Slot 6: Stabilized | ❌ | Default −1 (unassigned). Same Taranis QX7 scheme. |
| `COM_FLTT_LOW_ACT` | 1 | Warning when remaining flight time is low | ✅ | Default 1 (Warning) on main; the 1.16.2 default was 3 (Return), which is what this document used to use. The new default is accepted, so a drone that previously returned now only warns. Options: 0 None, 1 Warning, 3 Return. It should hardly ever matter since the Park is so small. What is critical is that the return heights stay below the net, which is covered by `RTL_RETURN_ALT` and `RTL_DESCEND_ALT`. |
| `COM_HOME_EN` | 1 | Home position set automatically | ✅ | Default 1 (enabled). PX4 sets the home position automatically when possible (per Max, on arm or boot). Requires reboot. Home cannot be reset without arming, which is one reason the geofence altitude limit is not used (see `GF_MAX_VER_DIST`). |
| `COM_HOME_IN_AIR` | 0 | Home is never set in the air | ✅ | Default 0 (disabled). If enabled, the autopilot may set its home position after takeoff (back-computed from the local position when one is available). Disabled so that home is never set while flying. |
| `COM_LOW_BAT_ACT` | 2 | Land mode | ❌ | Default 0 (Warning only). Land instead of just warning at critical battery. Option 4 (return at the critical level, terminate at the emergency level) is new on main and not used. |
| `COM_OBL_RC_ACT` | 4 | Land mode (on offboard loss) | ❌ | Default 0 (Position mode). Note: this is the *offboard*-loss action, not RC loss (see `NAV_RCL_ACT`). |
| `COM_OF_LOSS_T` | 0.5 | 0.5 s offboard-loss timeout | ❌ | Default 1.0 s. Lowering makes crashes less likely during offboard network dropouts since the failsafe triggers faster. Too low may make this sensitive to network lag, but lower than 0.5 should be tested for feasibility. |
| `COM_POS_FS_EPH` | 5 m | Failsafe above 5 m horizontal position error | ✅ | Default 5 m (−1 disables). The horizontal position error (EPH) above which PX4 triggers a failsafe; once the error has been below the threshold, a factor of 2.5 is applied before the position is invalidated. Kept at default because the offboard code should land, or refuse to arm, whenever the GPS fix type is not 6 (RTK fixed), long before PX4's own failsafe matters. |
| `COM_POS_LOW_ACT` | 5 | Land on a low position accuracy | ❌ | Default 3 (Return). The action taken when the position accuracy is worse than the `COM_POS_LOW_EPH` threshold (0 None, 1 Warning, 2 Hold, 3 Return, 4 Terminate, 5 Land). Set to Land so that a poor position estimate lands the vehicle instead of returning it. Per the v1.16.2 description the action is only executed in Mission or Hold (loiter) modes, and otherwise it is only a warning; while `COM_POS_LOW_EPH` is disabled it has no effect at all. |
| `COM_POS_LOW_EPH` | −1 m | Low accuracy failsafe disabled | ✅ | Default −1 (disabled). Threshold for `COM_POS_LOW_ACT`. The local position must still be valid for it to apply, which requires some velocity aiding or a large dead-reckoning time (`EKF2_NOAID_TOUT`), together with a high `COM_POS_FS_EPH`. No motivation to change. |
| `COM_PREARM_MODE` | 0 | Prearm state disabled | ✅ | Default 0 (disabled). The prearmed state is an intermediate state between disarmed and armed in which non-throttling actuators are active; the options are 0 disabled, 1 safety button, 2 always. The prearm feature is not used here. Option 1 is labelled "When safety off" on main. |
| `COM_RC_IN_MODE` | 3 | RC or MAVLink, keep first | ✅ | Default is 3 on main and in 1.16.2. Labelled "RC or MAVLink keep first until reboot" on main ("RC or Joystick keep first" in 1.16.2); "Joystick" is now "MAVLink" in the labels, and priority modes 5 to 8 are new. |
| `COM_RC_LOSS_T` | 0.5 s | RC counted as lost after 0.5 s without input | ✅ | Default 0.5 s. Time without a new setpoint from the RC or a joystick after which the connection is considered lost. It must be short, because the vehicle keeps using the last supplied setpoint until the timeout triggers. |
| `COM_RCL_EXCEPT` | 7 | Mission, all auto modes, and Offboard | ❌ | Default 0 (no exceptions). Bitmask to specify where to ignore loss of manual control and **not** trigger the failsafe specified in `NAV_RCL_ACT`. **The bits changed since 1.16.2:** bit 0 Mission, bit 1 "Auto modes" (was Hold only; now Hold, Takeoff, Land, Return, Descend, Follow Target, Precland and Orbit), bit 2 Offboard, and new bits 3 (external mode) and 4 (altitude cruise). Value 7 therefore now also ignores RC loss during Takeoff, Land, Return and the other auto modes, not only Mission, Hold and Offboard. Required for multi-agent setups since we only have one RC, but consider reverting to default when testing single-agent; RC then becomes required again. |
| `COM_SPOOLUP_TIME` | 1.0 s | 1.0 s spool-up after arming | ✅ | Default 1.0 s. The minimum time from arming the motors until the vehicle can be moved: the motors and propellers spool up to idle before being commanded faster, and the ESCs and smart batteries have time for their failure checks. Commands to move the vehicle are not applied until this time has passed after arming. No motivation to change. |
| `COM_VEL_FS_EVH` | 1 m/s | Failsafe above 1 m/s horizontal velocity error | ✅ | Default 1 m/s. The horizontal velocity error (EVH) above which PX4 triggers a failsafe, with the same factor of 2.5 between validating and invalidating as `COM_POS_FS_EPH`. No motivation to change. |
| `COM_WIND_MAX` | −1 m/s | High wind failsafe disabled | ✅ | Default −1 (disabled). The estimated wind speed above which the action in `COM_WIND_MAX_ACT` is triggered. No motivation to change; just do not fly in wind. |
| `COM_WIND_MAX_ACT` | 0 | No high wind action | ✅ | Default 0 (None). The action taken at `COM_WIND_MAX` (1 Warning, 2 Hold, 3 Return, 4 Terminate, 5 Land). No motivation to change. |
| `COM_WIND_WARN` | −1 m/s | Wind warning disabled | ✅ | Default −1 (disabled). When enabled, a warning is sent every minute while the estimated wind speed is above this value. No motivation to change. |


## EKF2: Estimator

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `EKF2_EV_CTRL` | 0 | External vision fusion disabled | ✅ | Default 0. Only relevant if a motion-capture system outdoors or a computer-vision camera aids the position estimate. This quad and workspace has neither. The sample drone had 15 (all four bits: horizontal position, vertical position, 3D velocity, yaw); Max is surprised by that and does not know who set it. Per the v1.16 source this is not limited to mocap or cameras: it applies to any vision/odometry input PX4 receives (for example MAVLink `VISION_POSITION_ESTIMATE` or `ODOMETRY`, which a companion computer could send). |
| `EKF2_EV_DELAY` | 0 ms | No external vision delay | ✅ | Default 0 ms. Delay of the external vision estimate relative to the IMU. Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. Requires reboot. |
| `EKF2_EV_NOISE_MD` | 0 | EV-reported variance | ✅ | Default 0 (the measurement noise comes from the vision message, with the EV noise parameters as a lower bound; 1 uses the noise parameters directly). Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. |
| `EKF2_EV_POS_X` | 0.000 m | Vision sensor at the CG on X | ✅ | Default 0.0. Position of the vision sensor focal point in the body frame. Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. |
| `EKF2_EV_POS_Y` | 0.000 m | Vision sensor at the CG on Y | ✅ | Default 0.0. Position of the vision sensor focal point in the body frame. Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. |
| `EKF2_EV_POS_Z` | 0.000 m | Vision sensor at the CG on Z | ✅ | Default 0.0. Position of the vision sensor focal point in the body frame. Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. |
| `EKF2_EV_QMIN` | 0 | No minimum vision quality | ✅ | Default 0 (range 0 to 100). Minimum quality metric, an optional field some VIO systems provide, for external vision to be started and fused. Only relevant if a motion-capture system or a computer-vision camera aids PX4 in estimating pose and twist, which this vehicle does not use (`EKF2_EV_CTRL` = 0); RTK makes such sources likely unnecessary anyway. |
| `EKF2_EVV_NOISE` | 0.1 m/s | Vision velocity noise 0.1 m/s | ✅ | Default 0.1 m/s. Measurement noise for vision velocity measurements, used to lower bound or replace the uncertainty in the message. No motivation to change, and it is not relevant without external vision such as mocap anyway. |
| `EKF2_GPS_CTRL` | 7 | Lon/lat + altitude + 3D velocity fusion | ✅ | Default 7. Dual-antenna heading (bit 3) stays off. Fusion also needs bit 0 of `EKF2_SENS_EN` (see below). |
| `EKF2_HGT_REF` | 1 | GPS is the height reference | ✅ | Default 1. This was contentious. The Astro's GPS vertical fix is much better than the Homebrew's, so without RTK the Homebrew tends to wander vertically when holding position in Position Mode (e.g., 0.5-1 m). Choosing 2 (range sensor) looks like a fix but makes `global_position_invalid` always true, so transitions into modes such as Hold are declined. This has the consequene that the drone gets stuck taking off (can never transition to Hold from Takeoff) or that **it cannot land** when using a ROS 2 teleop node if the code first dictates a transition to Hold mode. Hence: use RTK for better estimates and keep 1 so `global_position_invalid` stays false. (This is the lab's observation; I have not verified the `global_position_invalid` behaviour in the PX4 source. The source does say the range-sensor option should only be used over a flat surface, because the local NED origin then moves with ground level.) |
| `EKF2_IMU_POS_X` | 0.0587 m | IMU 0.0587 m forward of CG | ❌ | Default 0.0. Max does not know who set this or where the value came from. |
| `EKF2_IMU_POS_Y` | 0.000 m | IMU on centerline | ✅ | Default 0.0. |
| `EKF2_IMU_POS_Z` | 0.000 m | IMU at CG height | ✅ | Default 0.0. |
| `EKF2_MAG_CHECK` | 1 | Magnetic field strength check only | ✅ | Default 1 (strength only). Bitmask of the checks that decide whether the magnetometer data is valid: bit 0 field strength (tolerance `EKF2_MAG_CHK_STR`, 0.2 gauss), bit 1 field inclination (`EKF2_MAG_CHK_INC`, 20 degrees), bit 2 wait for GNSS to provide the theoretical strength and inclination from the World Magnetic Model (WMM). If GNSS data is received the field is compared with the WMM, otherwise with an average value. The check is useful to reject occasional hard-iron disturbances, and with `COM_ARM_MAG_STR` = 1 a failed check denies arming. Max would enable all the checks (7), but everything works and he has never broken a magnetometer in a crash, so there is no motivation to move away from the default. |
| `EKF2_MIN_RNG` | 0.01 m | Expected ground range 0.01 m | ✅ | Default 0.01 m on main (it became the default in 1.17.0; 1.16.2 had 0.1 m). The range finder reading the estimator assumes when the vehicle is on the ground and not moving, and the range finder returns invalid data or none, for example because it is inside its minimum measurement distance. The terrain estimator then still has a terrain height at the start of flight. Max applied 0.01 m (the lowest allowed value) early on 1.16.2 because he expected it to become the default; that is now confirmed in source. |
| `EKF2_MULTI_IMU` | 3 | Run 3 EKFs, one per IMU | ❌ | Default 0 (disabled). The flight controller has 3 IMUs inside, and letting PX4 pick the best estimate among them is a good idea. Requires `SENS_IMU_MODE` = 0. Requires reboot. PX4 only rewrites this value itself when it is outside 1 to 4 while `SENS_IMU_MODE` is 0. |
| `EKF2_MULTI_MAG` | 0 | Multi-EKF magnetometers disabled | ✅ | Default 0 (disabled). Maximum number of magnetometers to use for Multi-EKF; it requires `SENS_MAG_MODE` = 0 and a reboot. Left disabled because, unlike the IMUs, Max reports that the Cube does not have multiple magnetometers. The Here4 also provides a compass over DroneCAN (`UAVCAN_SUB_MAG`), so PX4 sees more than one. As far as I can tell, the sensors module chooses between them by priority and health (see the `CAL_MAGn_PRIO` parameters), not through `UAVCAN_ENABLE`. Max thinks both are reasonably accurate but is not sure which one is in use. If magnetometer issues appear, this is a good place to start. |
| `EKF2_OF_CTRL` | 1 | Optical flow fusion enabled | ✅ | Default is 1 in v1.16. Kept explicit so flow is always used. Flow data arrives over CAN (see `UAVCAN_SUB_FLOW`). Must match bit 2 of `EKF2_SENS_EN`: a source is fused only if its `EKF2_SENS_EN` bit and its own control parameter are both nonzero. |
| `EKF2_OF_POS_X` | 0.04440 m | Flow sensor 0.0444 m forward of CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_OF_POS_Y` | 0.06670 m | Flow sensor 0.0667 m right of CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_OF_POS_Z` | 0.05080 m | Flow sensor 0.0508 m below CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_RNG_A_HMAX` | 5.0 m | Range aid up to 5.0 m height | ✅ | Default 5.0 m (range 1 to 10). Maximum height above ground for the conditional range aid (`EKF2_RNG_CTRL` = 1): above it the estimator stops fusing the range finder for height. |
| `EKF2_RNG_A_VMAX` | 1.0 m/s | Range aid up to 1.0 m/s horizontal speed | ✅ | Default 1.0 m/s (range 0.1 to 2). Maximum horizontal speed for the conditional range aid (`EKF2_RNG_CTRL` = 1): above it the estimator stops fusing the range finder for height. |
| `EKF2_RNG_CTRL` | 1 | Range finder enabled (conditional mode) | ✅ | Default 1. Range aiding is used at low speed and low altitude (takeoff/landing). Must match bit 9 of `EKF2_SENS_EN` (this parameter must stay 1 or 2 while that bit is set). |
| `EKF2_RNG_POS_X` | −0.00635 m | Rangefinder 0.00635 m behind CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_RNG_POS_Y` | 0.0539 m | Rangefinder 0.0539 m right of CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_RNG_POS_Z` | 0.114 m | Rangefinder 0.114 m below CG | ❌ | Default 0.0. Sensor mounting offset. |
| `EKF2_SENS_EN` | 1797 | GNSS 0, optical flow, barometer, range finder, magnetometer | ❌ | Default 8191 (all 13 sources). New on main: a bitmask of which sensor fusion sources are enabled, applied only while disarmed (`EKF2::initFusionControl()`; in flight use the MAVLink command or the individual `*_CTRL` parameters). A source is fused only if **both** its `EKF2_SENS_EN` bit and its own control parameter are nonzero (`intended() = enabled && available`, where `available` comes from `EKF2_GPS_CTRL`, `EKF2_OF_CTRL`, `EKF2_RNG_CTRL`, `EKF2_BARO_CTRL`, `EKF2_MAG_TYPE` and so on), so a mismatch silently disables a source. Bit map below. Value 1797 = 0b0011100000101. **Not 1798**: that string (0b0011100000110) clears bit 0 (GNSS 0 off) and sets bit 1 (GNSS 1 on). |


### `EKF2_SENS_EN` bit map for the Homebrew

Bit numbers and names are from the main `module.yaml` and the `SensEn` enum in `EKF2.hpp`.

| Bit | Source | Set | Why |
|---:|---|:---:|---|
| 0 | GNSS 0 | 1 | The Here4. `EKF2_GPS_CTRL` is 7, so it matches. |
| 1 | GNSS 1 | 0 | There is no second GPS and we do not want PX4 to think there is one. That GPS still loads and works with this bit off needs an in-person test. |
| 2 | Optical flow | 1 | Must match `EKF2_OF_CTRL` (1). |
| 3 | External vision | 0 | RTK is good enough that feeding PX4 e.g. on-board computer vision would only confuse it, and the Park has no mocap. Matches `EKF2_EV_CTRL` = 0. |
| 4 to 7 | Aux global position 0 to 3 | 0 | Nothing like this on the vehicle. |
| 8 | Barometer | 1 | Very important source of height estimates. `EKF2_BARO_CTRL` is at its default of 1. |
| 9 | Range finder | 1 | Must match `EKF2_RNG_CTRL` being enabled (1 or 2). It is 1. |
| 10 | Magnetometer | 1 | Critical for estimation. `EKF2_MAG_TYPE` is at its default (Automatic). |
| 11 | Airspeed | 0 | Quadcopters, no airspeed sensor. |
| 12 | Ranging beacon | 0 | No ranging beacon. |

Bits 0, 2, 8, 9 and 10 set: 1 + 4 + 256 + 512 + 1024 = **1797**.

Max is not fully sure how this bitmask should be matched with `EKF2_OF_CTRL` and `EKF2_RNG_CTRL`. The source shows the AND behaviour described above, but how it plays out on the real vehicle is exactly what the test flight is for.

## FD: Failure Detector

The actuator (motor) failure check moved into the ESC arming checks on main (`escCheck.cpp`). Its parameters were replaced: `FD_ACT_MOT_C2T`, `FD_ACT_MOT_THR` and `FD_ACT_MOT_TOUT` no longer exist and are superseded by `MOTFAIL_C2T`, `MOTFAIL_OFF` and `MOTFAIL_TIME` (no value migration). `FD_ACT_EN` still exists, but its default flipped from 1 to 0. Everything here stays at its default. Per the main description the check only works for ESCs that report current consumption; the notes for `COM_ARM_CHK_ESCS` say these ESCs do not, so with the check enabled it would be inert at best.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `FD_ACT_EN` | 0 | Actuator failure check disabled | ✅ | Default 0 (disabled) on main; it was 1 in 1.16.2. If enabled, the HealthAndArmingChecks verify that each motor draws a minimum ESC current per throttle level, otherwise this indicates a motor failure. Leave at default. |

## GF: Geofence

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `GF_ACTION` | 5 | Land mode on geofence violation | ❌ | Default 2 (Hold mode). Land immediately rather than hover. |
| `GF_MAX_VER_DIST` | 0 m | Disabled | ✅  | Default 0 (disabled). **Do not** use this feature. Because the GPS fix moves during the 1-10 minute initial RTK fix, the relative altitude (relative to the fix when it first boots) will make the quadcopter think it's all over the place. Since you cannot reset the home position without arming, using this feature to prevent the quadcopter from hitting the net as an extra safety feature is moot. Just use CBFs. This feature would interfere with CBF offboard code anyways. If not using RTK (you should really just use it), the estimates are likely not good enough to prevent you from hitting the net. And, PX4's geofence does not take into account for instance the speed at which you approach a geofence, so it's not even enforceable as a never-cross-this boundary. |

## GNSS: GNSS Quality Requirements

New on main. The receiver selection, the per-receiver antenna offsets and delays (`SENS_GNSS0_*`, see the SENS section) and the quality checks moved from EKF2 to the sensors module (`vehicle_gps_position`). The `GNSS_REQ_*` thresholds are the "strict" checks that qualify a receiver, mainly before arming. Once the strict checks have passed on the ground, the checks that decide while armed are the "relaxed" ones with fixed limits: at least a 3D fix, at most 50 m position accuracy and 10 m/s speed accuracy (`gnss_checks.cpp`). They replace `EKF2_GPS_CHECK` and `EKF2_REQ_*`. `GNSS_REQ_TIME` (default 10 s, the continuous healthy time required at startup) is new too and is left at its default.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `GNSS_CHECK` | 2047 | All checks except jamming | ✅ | Default 2047 (range 0 to 4095). Replaces `EKF2_GPS_CHECK` (1023 in 1.16.2, bits 0 to 9). Bits: 0 satellite count, 1 PDOP, 2 EPH, 3 EPV, 4 speed accuracy, 5 horizontal position drift, 6 vertical position drift, 7 horizontal speed offset, 8 vertical speed offset, 9 spoofing, **10 GNSS fix type (new)**, 11 jamming (off). The automatic migration would carry 1023 over, which leaves bit 10 off and `GNSS_REQ_FIX` unenforced, so 2047 is set explicitly. Most 1.16.2 tests were done with 245 and without RTK, because Max did not yet know what he was doing. |
| `GNSS_REQ_EPH` | 3.0 m | Maximum 3.0 m horizontal position error to use GNSS | ✅ | Default 3.0 m (range 0.1 to 100; it was 2 to 100 as `EKF2_REQ_EPH`). Replaces `EKF2_REQ_EPH`. Maximum horizontal position error (EPH) the receiver may report (bit 2 of `GNSS_CHECK`). On its own this threshold does not require RTK; `GNSS_REQ_FIX` does. |
| `GNSS_REQ_EPV` | 5.0 m | Maximum 5.0 m vertical position error to use GNSS | ✅ | Default 5.0 m (range 0.1 to 100; 2 to 100 as `EKF2_REQ_EPV`). Replaces `EKF2_REQ_EPV`. Maximum vertical position error (EPV) the receiver may report (bit 3 of `GNSS_CHECK`). |
| `GNSS_REQ_FIX` | 6 | RTK fixed required | ❌ | Default 3 (3D fix). New on main, no 1.16.2 equivalent. Values: 0 none, 2 2D, 3 3D, 4 RTCM code differential, 5 RTK float, 6 RTK fixed, 8 extrapolated. The strict check fails when the reported fix type is below this value (`gnss_checks.cpp`) and only runs if bit 10 of `GNSS_CHECK` is set. Max set 6 so that nobody flies without RTK any more: with `COM_ARM_WO_GPS` = 0 arming is denied unless the receiver reports RTK fixed. **Scope:** this is a strict check. While armed, only the relaxed checks decide (3D fix minimum), so losing RTK in flight does not by itself trip it; the offboard code should still land when the fix type drops below 6, as before. |
| `GNSS_REQ_HDRIFT` | 0.1 m/s | Maximum 0.1 m/s horizontal drift to use GNSS | ✅ | Default 0.1 m/s (range 0.1 to 1.0, so this is also the strictest allowed value). Replaces `EKF2_REQ_HDRIFT`. Used for the horizontal position drift and horizontal speed offset checks (bits 5 and 7 of `GNSS_CHECK`), which only run when the vehicle is on the ground and stationary. |
| `GNSS_REQ_NSATS` | 6 | At least 6 satellites to use GNSS | ✅ | Default 6 (range 4 to 12). Replaces `EKF2_REQ_NSATS`. Minimum satellite count (bit 0 of `GNSS_CHECK`). |
| `GNSS_REQ_PDOP` | 2.5 | Maximum PDOP 2.5 to use GNSS | ✅ | Default 2.5 (range 1.5 to 5.0). Replaces `EKF2_REQ_PDOP`. Maximum position dilution of precision (bit 1 of `GNSS_CHECK`). |
| `GNSS_REQ_SACC` | 0.5 m/s | Maximum 0.5 m/s speed accuracy to use GNSS | ✅ | Default 0.5 m/s (range 0.5 to 5.0, so this is also the strictest allowed value). Replaces `EKF2_REQ_SACC`. Maximum speed accuracy (bit 4 of `GNSS_CHECK`). Per the main description, EKF2 also uses this limit for feeding GNSS velocity to the EKF-GSF yaw estimator and for trusting GNSS vertical velocity while the accelerometer clips, in flight too. No motivation to change. |
| `GNSS_REQ_VDRIFT` | 0.2 m/s | Maximum 0.2 m/s vertical drift to use GNSS | ✅ | Default 0.2 m/s (range 0.1 to 1.5). Replaces `EKF2_REQ_VDRIFT`. Used for the vertical position drift and vertical speed offset checks (bits 6 and 8 of `GNSS_CHECK`), which only run when the vehicle is on the ground and stationary. |

## GPS: Serial GPS

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `GPS_1_CONFIG` | 0 | Serial GPS driver disabled | ❌ | Default 201 (GPS 1). The GPS is the Here4 on DroneCAN, so the serial GPS driver stays off. |

## MAN: Manual Control

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MAN_ARM_GESTURE` | 0 | Stick arm/disarm gesture disabled | ❌ | Default 1 (enabled). Prevents accidental arming/disarming by stick position. |
| `MAN_KILL_GEST_T` | −1 | Kill stick gesture disabled | ✅ | Default −1 (negative value disables the feature). |
| `MAN_OVERRIDE_SPD` | 1.0 /s | Stick override on, 1.0 stick travel per second | ✅ | Default 1.0 (range -1 to 10; negative disables). Replaces `COM_RC_OVERRIDE` (3 in 1.16.2: auto and offboard modes) and `COM_RC_STICK_OV` (30 %). In auto and offboard modes, on a multicopter, the pilot takes over (Position mode, or Altitude if position is unavailable) when any of the four sticks moves faster than this threshold for several consecutive samples (`ManualControl.cpp`, `Commander::manualControlCheck()`). It measures stick speed in stick travel per second, not a 30 % displacement, so the sensitivity is not equivalent to the old setting; Max accepted the default. It is considered more important than stick nudging (see `MPC_AUTO_NUDGING`). |

## MAV: MAVLink

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MAV_0_CONFIG` | 101 | MAVLink instance 0 on TELEM 1 | ✅ | Default 101 (TELEM 1). The QGC telemetry radio connects here. Requires reboot. If torque-level control is ever wanted, note that (per Max, not verified by me) MAVROS does not support torque-level commands but uXRCE-DDS does, while RTK is not possible over uXRCE-DDS on main because there is no topic for it yet. The open PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368) (the branch under test on 2026-10-22, not merged) adds `/fmu/in/rtcm_corrections` (`px4_msgs/msg/RtcmData`) to the uXRCE-DDS client, which would remove the need to run MAVROS next to it for RTK. Torque-level control plus RTK would therefore need uXRCE-DDS and MAVROS running together. That would need a third serial port, because TELEM 1 and TELEM 2 are taken by the QGC radio and the Jetson link, and giving up the QGC radio is extremely dangerous for a torque-level offboard flight. Options are to wait until uXRCE-DDS supports RTK or MAVROS supports torque-level control, to write custom PX4 topics for RTK over uXRCE-DDS, or to solder a new cable and run uXRCE-DDS on another port such as GPS 2 (not tried). |
| `MAV_1_CONFIG` | 102 | MAVLink instance 1 on TELEM 2 | ❌ | Default 0 (disabled). The FTDI-to-USB cable to the Jetson connects to the flight controller here. Requires reboot. |
| `MAV_1_FLOW_CTRL` | 2 | Serial flow control auto-detected | ✅ | Default 2. The Jetson link. This setting tells PX4 to auto-detect flow control; PX4 does not write the parameter itself. Use 0 or 1 only if auto-detection fails. Requires reboot. |
| `MAV_1_FORWARD` | 0 | No message forwarding from the Jetson link | ✅ | Default 0. Broadcast messages (or ones aimed at another system) arriving on the Jetson link are not forwarded to the other MAVLink links. Requires reboot. |
| `MAV_1_MODE` | 2 | Onboard message set | ✅ | Default 2 (Onboard). The set of streamed messages on the Jetson link is the one meant for a companion computer. Requires reboot. |
| `MAV_1_RATE` | 0 B/s | Rate limit chosen from the baud rate | ✅ | Default 0. With 0, PX4 uses half the theoretical bandwidth, baud/20 bytes per second; at 921600 baud that is 46080 B/s. PX4 does not write the parameter itself. Requires reboot. |
| `MAV_PROTO_VER` | 2 | Always use MAVLink 2 | ✅ | Default is 2 on main (it was 0 in 1.16.2: start with MAVLink 1 and switch to 2 if the GCS sends version 2). Option 0 no longer exists; option 1 is now "Version 1 with auto-upgrade to v2 if detected". Not super critical. |
| `MAV_SYS_ID` | TBD (2–249) | Unique number per homebrew vehicle | ❌ | Default 1. **Never use 1** (every Astro requires 1 and it can't be changed). Choosing 1 will cause ROS 2 topic to intermingle between the Astro and Homebrew despite being namespaced. Must be unique. Range 1–250; never pick 250. Requires reboot. |
| `MAV_TYPE` | 2 | Quadrotor | ✅ | MC default 2 (metadata 0, generic micro air vehicle, overridden by `rc.mc_defaults`). The airframe type announced over MAVLink. Not super critical. |

## MC: Multicopter Autotune

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MC_AT_EN` | 1 | Autotune module enabled | ❌ | Default 0 (disabled). Allows autotuning the control cascade from QGC. This does **not** mean the quad tunes continuously in flight. Do not run it unless there is a reason to suspect poor control performance, which there really should not be. |

## MIS: Mission
| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MIS_TAKEOFF_ALT` | 2.5 m | Take off to 2.5 m from ground level  | ✅ | Default 2.5 m. Take off to 2.5 m from ground level |


## MOTFAIL: Motor Failure

Replacement parameters for `FD_ACT_MOT_*`. All stay at their defaults and are inert while `FD_ACT_EN` is 0. The main descriptions of these three still mention the old `FD_ACT_*` names, so read them with that in mind.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MOTFAIL_C2T` | 35 A/% | Current-to-throttle scale 35 A/% | ✅ | Default 35 (range 0 to 50). The slope between the expected steady-state current and the linearized, normalized thrust command. The old `FD_ACT_MOT_C2T` default was 2, so the number is not comparable. Leave at default. |
| `MOTFAIL_OFF` | 10 A | Over/under-current offset 10 A | ✅ | Default 10 A (range 0 to 30). The check triggers if the difference between the expected and measured current is above this value. Leave at default. |
| `MOTFAIL_TIME` | 1.0 s | Violation must last 1.0 s | ✅ | Default 1.0 s (range 0.01 to 10). The current thresholds must be exceeded for this long before a motor failure triggers. The old `FD_ACT_MOT_TOUT` was in milliseconds (default 100). Leave at default. |

## MPC: Multicopter Position Control

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `MPC_AUTO_NUDGING` | 0 | Stick nudging in auto modes disabled | ✅ | Default 0. Replaces `MPC_LAND_RC_HELP` (0 in 1.16.2, so nothing is lost; a nonzero old value would have migrated to bit 1). Bitmask: bit 0 yaw nudging in all auto modes, bit 1 landing nudging (pitch/roll move the vehicle horizontally, the throttle stick scales the descent speed from 0 to 2 times `MPC_LAND_SPEED`, yaw rotates the heading). Deliberately left off: the main description says stick override must be disabled (`MAN_OVERRIDE_SPD` = -1) for nudging to work, and `Commander::manualControlCheck()` has no exception for nudging, so the two are mutually exclusive in practice. Max prefers the override. Other points from the 1.16.2 reasoning that still apply if this is ever enabled: the throttle stick on a Taranis QX7 does not spring back to center, so an RC left on with throttle low would double the descent speed of every Land, including a battery failsafe Land (`COM_LOW_BAT_ACT`) (my inference from the description), and it has no effect in Offboard. `MPC_LAND_RADIUS`, which limits how far landing nudging can move the quad, now defaults to -1 (no limit); it was 1000 m in 1.16.2. |

## NAV: Navigator

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `NAV_DLL_ACT` | 0 | Disabled (no GCS-loss failsafe) | ✅ | Default 0. Removes the need for QGC to stay connected. Required for multi-agent setups. |
| `NAV_RCL_ACT` | 3 | Land mode on RC loss | ❌ | Default 2 (Return mode). Land in place instead of returning. Option 7 ("Hold mode (no failsafe)") is new on main and not used. |

## PLD: Precision Landing

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `PLD_SRCH_ALT` | 2.5 m | Climb to 2.5 m above home when searching for the landing target | ❌ | Default 10 m. Our flight space has a net at 8 m. |

## PWM: Motor Outputs

These are what the motors for this quadcopter need. Output functions 101 to 104 are Motor 1 to Motor 4.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `PWM_MAIN_FUNC1` | 101 | Motor 1 | ❌ | Default 0 (disabled). What the motors for this quadcopter need. |
| `PWM_MAIN_FUNC2` | 102 | Motor 2 | ❌ | Default 0 (disabled). What the motors for this quadcopter need. |
| `PWM_MAIN_FUNC3` | 103 | Motor 3 | ❌ | Default 0 (disabled). What the motors for this quadcopter need. |
| `PWM_MAIN_FUNC4` | 104 | Motor 4 | ❌ | Default 0 (disabled). What the motors for this quadcopter need. |
| `PWM_MAIN_MAX1` | 1900 | Output 1 maximum 1900 µs | ❌ | Default 2000. What the motors for this quadcopter need. |
| `PWM_MAIN_MAX2` | 1900 | Output 2 maximum 1900 µs | ❌ | Default 2000. What the motors for this quadcopter need. |
| `PWM_MAIN_MAX3` | 1900 | Output 3 maximum 1900 µs | ❌ | Default 2000. What the motors for this quadcopter need. |
| `PWM_MAIN_MAX4` | 1900 | Output 4 maximum 1900 µs | ❌ | Default 2000. What the motors for this quadcopter need. |
| `PWM_MAIN_MIN1` | 1100 | Output 1 minimum 1100 µs | ❌ | Default 1000. What the motors for this quadcopter need. |
| `PWM_MAIN_MIN2` | 1100 | Output 2 minimum 1100 µs | ❌ | Default 1000. What the motors for this quadcopter need. |
| `PWM_MAIN_MIN3` | 1100 | Output 3 minimum 1100 µs | ❌ | Default 1000. What the motors for this quadcopter need. |
| `PWM_MAIN_MIN4` | 1100 | Output 4 minimum 1100 µs | ❌ | Default 1000. What the motors for this quadcopter need. |

## RC: Radio Control

These are the Taranis QX7 template needed to use the radio with this quadcopter.

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `RC_CHAN_CNT` | 18 | 18 RC channels saved at RC calibration | ❌ | Default 0. Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_KILLSWITCH_TH` | 0.75 | Kill switch threshold 0.75 | ✅ | Default 0.75. Fine as is. |
| `RC_MAP_ARM_SW` | 9 | Arm switch on RC channel 9 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_MAP_AUX1` | 0 | AUX1 unassigned | ✅ | Default 0 (unassigned). Channel 10 is the kill switch (`RC_MAP_KILL_SW`), so AUX1 must not also use it. |
| `RC_MAP_FLTMODE` | 5 | Flight mode selection on RC channel 5 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_MAP_KILL_SW` | 10 | Kill switch on RC channel 10 | ❌ | Default 0 (unassigned). Channel 10 is the right switch on the Taranis QX7. On main, kill zeroes the motor outputs immediately (`mixer_module.cpp`). Flipping the switch back within 5 seconds restarts the motors; after 5 seconds the vehicle disarms. That 5 s is hardcoded (`COM_KILL_DISARM` no longer exists, see the removed-parameters table). **Be careful!!!** |
| `RC_MAP_PITCH` | 2 | Pitch on RC channel 2 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_MAP_ROLL` | 1 | Roll on RC channel 1 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_MAP_THROTTLE` | 3 | Throttle on RC channel 3 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |
| `RC_MAP_YAW` | 4 | Yaw on RC channel 4 | ❌ | Default 0 (unassigned). Taranis QX7 template needed to use this radio with the quadcopter. |

## RTL: Return Mode

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `RTL_DESCEND_ALT` | 2 m | 2 m (≈ 6.6 ft) | ❌ | MC default 10 m (metadata 30 m, overridden by `rc.mc_defaults`). The net is 8 m tall, so this keeps the vehicle clear of it. |
| `RTL_RETURN_ALT` | 2 m | 2 m (≈ 6.6 ft) | ❌ | MC default 30 m (metadata 60 m, overridden by `rc.mc_defaults`). The net is 8 m tall, so this keeps the vehicle clear of it. |

## SENS: Sensors

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `SENS_BOARD_ROT` | 2 | Autopilot board rotated Yaw 90° | ❌ | Default 0 (no rotation). Required for how the CubePilot is placed in the case. Requires reboot. |
| `SENS_EN_PMW3901` | 0 | Local PMW3901 optical flow driver disabled | ✅ | Default 0 (disabled). This enables a PMW3901 wired to the Cube's SPI bus. The optical flow sensor is on CAN instead (see `UAVCAN_SUB_FLOW`). |
| `SENS_EN_SF0X` | 8 | LW20/c | ❌ | Default 1 (SF02). Selects the model of the serial LightWare lidar. It only appears when `SENS_SF0X_CFG` is not disabled, so it does not need to be set (and is not in the `.params` file). |
| `SENS_EN_SF1XX` | 6 | SF/LW20/c | ❌ | Default 0 (disabled). The LW20/c on I2C is the only distance sensor used for estimation. Requires reboot. Options 8 (GRF250) and 9 (GRF500) are new on main; our value 6 is unchanged. |
| `SENS_FLOW_ROT` | 0 | No rotation | ✅ | Default 0 (no rotation). Rotation of the optical flow sensor relative to the airframe. It seems to work fine at 0, but **Max was not able to verify which direction the optical flow sensor faces**. |
| `SENS_GNSS0_DELAY` | 110 ms | GNSS 0 delay 110 ms | ✅ | Default 110 ms (range 0 to 300). Replaces `EKF2_GPS_DELAY`, which the migration copies to both `SENS_GNSS0_DELAY` and `SENS_GNSS1_DELAY`; only slot 0 is set here since there is no second receiver. The type changed from float to int32 with the rename. GNSS measurement delay relative to the IMU measurements. No motivation to change. |
| `SENS_GNSS0_OFFX` | 0.010 m | GNSS antenna 0.010 m forward of CG | ❌ | Default 0.0. Measured antenna offset. Replaces `EKF2_GPS_POS_X` (named `SENS_GPS0_OFFX` on release/1.18). **Slot matching:** the offset slot is matched to the receiver by device ID (`SENS_GNSS0_ID`). When all ID slots are 0 it falls back to the uORB instance index, which the main description calls "only reliable for serial GPS"; the Here4 is DroneCAN. If no slot matches, the offsets stay zero (`VehicleGPSPosition::findParamSlot`). `SENS_GNSS0_ID` is the receiver's device ID, a per-drone value, so it is not in the template. Bench-check that the offsets reach `vehicle_gnss.antenna_offset`. |
| `SENS_GNSS0_OFFY` | 0.000 m | GNSS antenna on centerline | ✅ | Default 0.0. Replaces `EKF2_GPS_POS_Y`. Same slot-matching caveat as `SENS_GNSS0_OFFX`. |
| `SENS_GNSS0_OFFZ` | 0.217 m | GNSS antenna 0.217 m below CG (body Z points down) | ❌ | Default 0.0. Measured antenna offset. Replaces `EKF2_GPS_POS_Z`. Same slot-matching caveat as `SENS_GNSS0_OFFX`. |
| `SENS_IMU_MODE` | 0 | Sensors hub does not select the primary IMU (needed for multi-EKF) | ❌ | Default 1 (publish primary IMU selection). Required by `EKF2_MULTI_IMU` = 3: the v1.16 description of `EKF2_MULTI_IMU` says "Requires SENS_IMU_MODE 0". Requires reboot. |
| `SENS_SF0X_CFG` | 0 | Disabled | ✅ | Default 0 (disabled). Serial port configuration for the LightWare lidar (that is, UART). Since the LW20/c is on I2C (`SENS_EN_SF1XX`), this stays disabled to prevent PX4 from getting confused. |

## SEP: Septentrio GPS

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `SEP_PORT1_CFG` | 0 | Septentrio driver disabled | ✅ | Default 0 (disabled). The GPS is the Here4 on DroneCAN, so the Septentrio serial driver stays off. |

## SER: Serial Ports

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `SER_TEL1_BAUD` | 57600 | TELEM 1 at 57600 baud | ✅ | Default 57600. The QGC telemetry radio on TELEM 1 (`MAV_0_CONFIG`); the radio must use the same baud rate. Requires reboot. |
| `SER_TEL2_BAUD` | 921600 | TELEM 2 at 921600 baud | ✅ | Default 921600. The Jetson link on TELEM 2 (`MAV_1_CONFIG`). Requires reboot. |

## SF1XX: LightWare Lidar (I2C)

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `SF1XX_MODE` | 1 | Enabled | ✅ | Default 1 (enabled). Operation mode of the LightWare lidar driver. The other option, 2 (disabled during VTOL fast forward flight), is for VTOL vehicles and is not relevant here. |

## SYS: System

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `SYS_AUTOSTART` | 4001 | Generic Quadcopter (airframe `4001_quad_x`) | ❌ | Default 0 (none). Uses the multicopter for PX4 default parameters. Requires reboot. |
| `SYS_HAS_BARO` | 1 | Barometer expected | ✅ | Default 1 (on). Pre-flight check for a barometer; if disabled, the preflight checks do not look for one. Requires reboot. |
| `SYS_HAS_GPS` | 1 | GPS expected | ✅ | Default 1 (on). Controls whether the vehicle has a GPS. If disabled, the sensors hub does not process `sensor_gps` at all and GPS is not available to the rest of the system, so this must stay on. Requires reboot. |
| `SYS_HAS_MAG` | 1 | One magnetometer expected | ✅ | Default 1 (on). Number of magnetometers the pre-flight check requires: 0 means none is expected, and 1 to N require N magnetometers to be present. Requires reboot. |
| `SYS_HAS_NUM_DIST` | 1 | One distance sensor required | ❌ | Default 0 (check disabled). The preflight check fails if fewer than this number of distance sensors with valid data are present. Set to 1 so that a missing or silent LW20/c is caught before flight. |
| `SYS_HAS_NUM_OF` | 1 | One optical flow sensor required | ❌ | Default 0 (check disabled). The preflight check fails if fewer than this number of optical flow sensors with valid data are present (the maximum is 1). Set to 1 so that a missing or silent flow sensor is caught before flight. |
| `SYS_USB_AUTO` | 2 | MAVLink starts on USB right away | ✅ | Default 2 (MAVLink). Per the PX4 serial configuration documentation, it selects whether the USB port runs no particular protocol, auto-detects the protocol, or is set to MAVLink. With MAVLink, PX4 starts MAVLink on USB as soon as USB is available instead of waiting to receive data first. Keep it at default so the USB link works right away. |

## THR: Thrust Model

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `THR_MDL_FAC` | 0.3 | Thrust model factor 0.3 (30% quadratic term) | ❌ | Default 0. Usually determined by a bench thrust test. This value is a good guess that works in flight, so there is no motivation to change it. |

## UAVCAN: DroneCAN

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `UAVCAN_ENABLE` | 2 | Sensors, automatic config | ❌ | Default 0 (disabled). DroneCAN must be on for the Here4 and the flow/rangefinder node. Value 2 allocates node IDs dynamically. Requires reboot. |
| `UAVCAN_PUB_RTCM` | 1 | Publish RTCM stream | ❌ | Default 0. Required for PX4 to accept RTK corrections over DroneCAN. Requires reboot. |
| `UAVCAN_RNG_MAX` | 100 m | Rangefinder maximum range 100 m | ❌ | Default 999 m. The maximum valid range accepted from a rangefinder connected over DroneCAN. 100 m is the rated maximum range of the LW20/c. As far as I can tell from the description, it only applies to a DroneCAN rangefinder (`UAVCAN_SUB_RNG`, which is 0 here) and not to the LW20/c on I2C. |
| `UAVCAN_RNG_MIN` | 0 m | Rangefinder minimum range 0 m | ✅ | Default 0 m. The minimum valid range accepted from a rangefinder connected over DroneCAN. Technically the rated minimum for the LW20/c is 0.2 m, but this works so it is fine. The same caveat as for `UAVCAN_RNG_MAX` applies. |
| `UAVCAN_SUB_FLOW` | 1 | Optical flow subscription enabled | ❌ | Default 0. The optical flow sensor is on the CAN bus. This subscribes to its flow data only; its distance sensor is controlled separately by `UAVCAN_SUB_RNG`. Requires reboot. |
| `UAVCAN_SUB_GPS` | 1 | GPS subscription enabled | ✅ | Default 1. The Here4 provides GPS over DroneCAN. Requires reboot. |
| `UAVCAN_SUB_IMU` | 0 | IMU subscription disabled | ✅ | Default 0. No external IMU on CAN; the IMUs are inside the Cube. Requires reboot. |
| `UAVCAN_SUB_MAG` | 1 | Magnetometer subscription enabled | ✅ | Default 1. The Here4 provides a compass over DroneCAN. Max is not sure this compass is actually the one being used (see `EKF2_MULTI_MAG`). Requires reboot. |
| `UAVCAN_SUB_RNG` | 0 | Range finder subscription disabled | ✅ | Default 0. The only distance sensor is the LW20/c on I2C. The optical flow sensor's own distance sensor must never be used for estimation. Requires reboot. |

## USB: USB MAVLink

| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `USB_MAV_MODE` | 2 | Onboard message set on USB | ✅ | Default 2 (Onboard). The MAVLink profile used on the USB port when MAVLink is set or detected (`SYS_USB_AUTO`). The PX4 documentation says the USB port is by default a MAVLink port with the onboard profile meant for companion computers, the same message set as `MAV_1_MODE`. |

## uXRCE: A MAVROS Alternative
| Parameter Name | Setting (Raw) | Setting (Word) | Is Default (MC) | Reason |
|---|---|---|:---:|---|
| `UXRCE_DDS_CFG` | 0 | Disabled | ✅ | Default 0. Turns on the UXRCE-DDS Client (alternative to MAVROS that allows torque-level control but foregoes RTK on main; PR #29368 adds an RTCM input topic, see `MAV_0_CONFIG`). |
| `UXRCE_DDS_DOM_ID` | 0 | ROS Domain ID | ✅ | Default 0. Must match ROS setup. |
| `UXRCE_DDS_PTCFG` | 2 | Custom participant | ❌ | Default 0. Required if using discovery server. Needs a XML config and file on fs/microsd/etc/. **This parameter only appears if `UXRCE_DDS_CFG` is not zero. Ignore if not using uXCRE.** |

## Removed or renamed since v1.16.2

Every name below was in the 1.16.2 template and does not exist on main. Verified by running the PX4 parameter metadata generator on both source trees.

| 1.16.2 parameter (value) | On main | What it means |
|---|---|---|
| `EKF2_GPS_POS_X` / `Y` / `Z` (0.01 / 0 / 0.217) | `SENS_GNSS0_OFFX` / `Y` / `Z` | Renamed twice (`SENS_GPS0_*` on release/1.18). Migrated automatically on import. |
| `EKF2_GPS_DELAY` (110) | `SENS_GNSS0_DELAY`, `SENS_GNSS1_DELAY` | Renamed; copied to both slots; float became int32. |
| `EKF2_GPS_CHECK` (1023) | `GNSS_CHECK` (2047) | Renamed, but the carried value would leave the new fix-type bit off; set explicitly. |
| `EKF2_REQ_EPH` / `EPV` / `HDRIFT` / `NSATS` / `PDOP` / `SACC` / `VDRIFT` | `GNSS_REQ_*` | Renamed, same defaults. |
| `MPC_LAND_RC_HELP` (0) | `MPC_AUTO_NUDGING` bit 1 | A nonzero value migrates; 0 does not. |
| `COM_RC_OVERRIDE` (3), `COM_RC_STICK_OV` (30) | `MAN_OVERRIDE_SPD` | Only `COM_RC_OVERRIDE` = 0 migrates (to -1); 3 is dropped silently. Different unit (stick travel per second). |
| `FD_ACT_MOT_C2T`, `FD_ACT_MOT_THR`, `FD_ACT_MOT_TOUT` | `MOTFAIL_C2T`, `MOTFAIL_OFF`, `MOTFAIL_TIME` | Replaced, no migration, different defaults and units. |
| `COM_KILL_DISARM` (0 s) | hardcoded 5 s | Removed by PR #26736 (commit `6b5147110b`, 2026-03-14, "remove needless parameter"). Kill still zeroes the motors immediately, but the vehicle now stays armed for 5 s, and flipping the switch back within that time restarts the motors. With 0 the disarm was immediate and the kill could not be undone. |
| `COM_ARM_SDCARD` (2) | hardcoded warning | A missing SD card never blocks arming now (`sdcardCheck.cpp` uses `NavModes::None`). The "no SD prevents arming" setting is lost. |
| `COM_POSCTL_NAVL` (1) | none | Removed in 1.17.0. Position mode falls back to Altitude, then Stabilized, never to Land. |
| `COM_DISARM_MAN` (1), `COM_TAKEOFF_ACT` (0), `COM_OBC_LOSS_T` (5), `COM_IMB_PROP_ACT` (0) | hardcoded | Our 1.16.2 values equal the new hardcoded behavior, so nothing is lost. |
| `BAT2_I_CHANNEL` (-1) | none | Removed together with `BAT1_I_CHANNEL`. |
