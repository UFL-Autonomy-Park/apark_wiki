---
title: "Case Study: Porting the Parameters to PX4 Main"
author: Max Gardenswartz
updated: 2026-11-03
status: active
status_note: Valid only for PX4 main at commit 5f429033bf on 2026-10-22. Do not use it to port to 1.18.0 or any other stable release.
applies_to: [apark]
assisted_by: Claude
glance: >-
  A worked example of porting the Homebrew parameter template from PX4 1.16.2 to PX4 main: the method, the kinds of changes you will meet, and the decisions made. Read it before upgrading the fleet.
---

**Date:** 2026-10-22. Max is flight-testing PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368) (RTCM corrections over uXRCE-DDS) on a real Homebrew quadcopter on a branch of PX4 `main`. The flights were a success, and the PR has since been merged. The feature is expected (likely) in PX4 1.19.0 as a stable feature.

!!! warning
    **Do not use this case study, or the files it produced, to port to 1.18.0 or any other stable release.** What was tested is `main` as of 2026-10-22 (commit `5f429033bf`, the 1.19 development line). `main` already differs from `release/1.18`, and it will differ from future stable releases. For example, `GNSS_CHECK`, `GNSS_REQ_*` and `SENS_GNSS0_*` exist only on `main`; `release/1.18` still has `EKF2_GPS_CHECK`, `EKF2_REQ_*` and `SENS_GPS0_*`. The point of this document is the **method and the kinds of decisions**, not the answers. Whoever upgrades the fleet must regenerate everything against the release they actually target.

## What This Is For

Someone, one day, will upgrade PX4 on every Homebrew quadcopter. The upgrade tutorial (written separately) tells you what to click. It does not tell you what to put in the parameter template, because that depends on what changed between the two PX4 versions. This case study shows one complete example of that part, for the parameters only, so a future graduate student knows what the work looks like.

The outputs of such a port are three things:

1. A new [Example Parameters for PX4 Main](example-parameters-for-px4-main.md): the reference with one row per parameter, why it has its value, and whether it is at the default.
2. A matching [example-parameters-px4-main.params](example-parameters-px4-main.params): the file you apply in QGroundControl after the airframe defaults are loaded.
3. A check of [Calibration Parameters](../calibration-and-per-drone-parameters.md): the list of parameters that are unique to each drone. If any of those names changed, that sensor has to be recalibrated after the upgrade.

## What Max Did

Max used an AI assistant (Claude) as a research helper, with one rule: **everything is verified against the PX4 source, nothing is guessed.** The assistant was not trusted for what it remembered about PX4. It was used to do the reading and diffing quickly, and every claim had to point at a file.

**What was fed in**

- [Parameters](../parameters.md): the 1.16.2 reference, 202 documented parameters.
- [homebrew-px4-v1.16.2.params](../homebrew-px4-v1.16.2.params): the 1.16.2 template of just parameters in the [Parameters](../parameters.md) page.
- [Calibration Parameters](../calibration-and-per-drone-parameters.md): the per-drone parameters that should never save transfered between drones but need to be ported/preserved during an update

**What was asked**

> These params are all what my quadcopter uses for PX4 1.16.2. I'm about to test something in the current mainline PX4 code. Which of these params have had their names changed or have been reworked? You must verify against source. Do not guess.

Then, after reading the findings, Max made a decision on each case (below) and asked for the new files.

## How the Comparison Against Source Was Done

This is the part to copy. Release notes and parameter descriptions were used only as leads.

1. **Pin the code.** Check out each version you care about as its own `git worktree`: the tag you came from (`v1.16.2`), and the version you are going to (here `main`, plus `v1.17.0` and `release/1.18` to understand the history).
2. **Generate the parameter metadata from each tree.** PX4 builds a `parameters.json` from the `*.yaml` / `*.c` parameter definitions (the `metadata_parameters` target in `cmake/metadata.cmake`). A full firmware build is not needed; the same generator scripts can be run directly (`Tools/serial/generate_config.py`, `Tools/module_config/generate_params.py`, `src/lib/parameters/px_process_params.py`). On 1.16.2 one extra argument was needed (`--inject-xml src/lib/parameters/parameters_injected.xml`).
3. **Diff the metadata.** For every parameter in your list: does the name exist? Same type? Same default, min, max, units? Same enum values and bitmask bits? That one script answered "renamed or removed?" for all 202 parameters at once. Result: 176 names survive, 26 do not.
4. **Read the migration code.** `src/lib/parameters/param_translation.cpp` (`param_modify_on_import`) is where PX4 renames old parameters automatically. Read it, do not assume. Check also *where it is called from* (see Renamed).
5. **Read what consumes the parameter.** A changed default or a deleted parameter only matters through the code that uses it, for example `Commander.cpp`, `sdcardCheck.cpp`, `battery.cpp`, `gnss_checks.cpp`, `mixer_module.cpp`, `ManualControl.cpp`.
6. **Diff the layered defaults.** The "Is Default" column in our document is not just the metadata default. It is the metadata default overridden by `rc.board_defaults` (Cube Orange), `rc.mc_defaults` and the airframe file `4001_quad_x`. Compare those files across versions too. Here none of them changed for the parameters in our document.
7. **Validate the new template mechanically.** A script checks every name in the new `.params` against the generated `parameters.json` of the target: it exists, the type matches, the value is inside min/max, enum values are legal. That check caught a real error (see "Renamed, and PX4 Migrates the Value").
8. **Only then judge.** Each finding gets a decision from a human.

## The Cases

Each case below is a *kind* of change you will meet again. The parameter names are just examples from this run.

### Renamed, and PX4 Migrates the Value

| 1.16.2 | `main` | Note |
|---|---|---|
| `EKF2_GPS_POS_X/Y/Z` | `SENS_GNSS0_OFFX/Y/Z` | Renamed twice: `SENS_GPS0_*` on `release/1.18`, then `SENS_GNSS0_*` on `main`. |
| `EKF2_GPS_DELAY` | `SENS_GNSS0_DELAY` (and `SENS_GNSS1_DELAY`) | The migration copies the value to both slots. |
| `EKF2_REQ_EPH/EPV/HDRIFT/NSATS/PDOP/SACC/VDRIFT` | `GNSS_REQ_*` | Same defaults. |
| `MPC_LAND_RC_HELP` | bit 1 of `MPC_AUTO_NUDGING` | Our value was 0, so nothing to carry. |

What to learn:

- **Release notes do not give a full picture of parameter changes.** Only some changes will be highlighted in the release notes. Many will not.
- **PX4 cannot migrate parameters for you.** PX4 has some code (`param_modify_on_import`) to try and "upgrade" old parameters, but you cannot rely on this. Manual re-selection and porting of all parameter is required. PX4 will silently get rid of old parameter names!
- **The type can change with the name.** `EKF2_GPS_DELAY` was a float (type 9 in the `.params` file); `SENS_GNSS0_DELAY` is an int32 (type 6). The mechanical validation in step 7 caught this.
- **A renamed parameter can have a new matching rule.** In this case study's upgrade, it happens to be that the antenna offsets are now matched to the receiver by device ID (`SENS_GNSS0_ID`). With all IDs at 0 PX4 falls back to the uORB instance index, which the parameter description itself calls "only reliable for serial GPS". Our Here4 is DroneCAN. If no slot matches, the offsets silently stay zero.

### Renamed, but the Migrated Value Does Not Mean What You Want

`EKF2_GPS_CHECK` (1023) became `GNSS_CHECK`. The same 1023 would be carried over, but `GNSS_CHECK` has a **new bit 10 (fix type)** and a new bit 11 (jamming). With 1023, bit 10 is off, so the new `GNSS_REQ_FIX` would never be enforced (which we want to enforce since this was not possible to enforce in 1.16.2). The new template sets `GNSS_CHECK` = 2047 (the default) explicitly.

Lesson: when a bitmask is renamed, compare the bit list, not just the name.

### Removed Completely, Behavior Now Hardcoded

| Removed | What it did for us | What is true on `main` |
|---|---|---|
| `COM_KILL_DISARM` = 0 | Disarm immediately after kill | Hardcoded 5 s. See the deep dive below. |
| `COM_ARM_SDCARD` = 2 | No SD card blocks arming | A missing SD card is only a warning. The setting is lost. |
| `COM_POSCTL_NAVL` = 1 | Land when position is lost in Position mode | Removed in 1.17.0. Falls back to Altitude, then Stabilized, never Land. |
| `COM_DISARM_MAN`, `COM_TAKEOFF_ACT`, `COM_OBC_LOSS_T`, `COM_IMB_PROP_ACT` | Our values equal the new hardcoded behavior | Nothing lost. |
| `BAT2_I_CHANNEL` | Default only | Gone with `BAT1_I_CHANNEL`. |

For every removed parameter ask two questions: **is our value the same as what is now hardcoded** (then nothing changes) and **if not, what do we lose** (then someone must decide). Max reviewed this list and accepted it, after considering `COM_KILL_DISARM` below.

**`COM_KILL_DISARM`.** It was the one that worried Max most. Kill still stops the motors immediately, but on `main` the vehicle no longer disarms at once: it stays armed for a hardcoded 5 s, and flipping the kill switch back in that time restarts the motors. The parameter was removed in PX4 PR [#26736](https://github.com/PX4/PX4-Autopilot/pull/26736). An irreversible kill was wanted to minimize the consequences of reactivating a killed drone, but the new behavior is acceptable. **Pilots must now remember that after landing on a kill, they cannot deactivate kill too quickly: if kill was set less than 5 seconds ago, the drone can take off again.** Max verified the new kill-switch logic in the test flights.

### Replaced by a Differently Shaped Parameter, No Migration

- `COM_RC_OVERRIDE` (3: auto and offboard) and `COM_RC_STICK_OV` (30 %) became **`MAN_OVERRIDE_SPD`**. Only `COM_RC_OVERRIDE` = 0 migrates (to -1); our 3 would have been dropped silently. The unit changed from a 30 % displacement to stick *travel per second* (default 1.0), so the old "30" cannot be converted. In code (`ManualControl.cpp`, `Commander::manualControlCheck()`) any of the four sticks moving faster than the threshold, in auto or offboard mode on a multicopter, switches to Position mode.
- `FD_ACT_MOT_C2T`, `FD_ACT_MOT_THR`, `FD_ACT_MOT_TOUT` became `MOTFAIL_C2T`, `MOTFAIL_OFF`, `MOTFAIL_TIME`. No migration, different defaults (the C2T default went from 2 to 35) and a different time unit. Our policy for these was "leave at default", so we use the new defaults.

### Same Name, New Default

Our reference documents "Is Default" for every row, and many rows said "left at the default". When the default moves, those rows move with it unless a human says otherwise.

| Parameter | 1.16.2 default | `main` default | Decision |
|---|---|---|---|
| `BAT1/2/3_V_CHARGED` | 4.05 V | 4.2 V | Accept 4.2 V (reasoning below). |
| `COM_FLTT_LOW_ACT` | 3 (Return) | 1 (Warning) | Accept the new default. |
| `FD_ACT_EN` | 1 | 0 | Accept the new default. |
| `EKF2_MIN_RNG` | 0.1 m | 0.01 m | Already 0.01 m. Now equals the default (the 1.16.2 note, "expected to become the default", is confirmed). |
| `MAV_PROTO_VER` | 0 | 2 | Already 2. Now equals the default. |

**Worked example: `BAT1_V_CHARGED`.** The old 4.05 V was a workaround. The voltage is measured on a quadcopter drawing about 5 A, and sag makes a full 4.2 V cell read about 4.05 V. On `main` the default is 4.2 V and the description no longer advises setting it lower. What does that do to the safety-critical thresholds? `battery.cpp` interpolates linearly between `V_EMPTY` (3.6 V) and `V_CHARGED`, so the same fractional thresholds now correspond to higher voltages:

| Threshold | Fraction | Voltage with 4.05 V | Voltage with 4.2 V |
|---|---:|---:|---:|
| `BAT_LOW_THR` | 0.35 | 3.76 V | 3.81 V |
| `BAT_CRIT_THR` | 0.25 | 3.71 V | 3.75 V |
| `BAT_EMERGEN_THR` | 0.15 | 3.67 V | 3.69 V |
| `COM_ARM_BAT_MIN` | 0.50 | 3.83 V | 3.90 V |

Every warning and the arming limit now trip earlier, which is more conservative. Max accepted it and left all four fractions unchanged. Two more consumers of `V_CHARGED` were found while reading `battery.cpp`: the over-voltage "spike" fault threshold (cells × `V_CHARGED` × 1.05) and the battery scale used only when `MC_BAT_SCALE_EN` is on (default 0, not set).

### Same Name, Changed Meaning

`COM_RCL_EXCEPT` = 7 is a bitmask. Bit 1 meant "Hold" in 1.16.2; on `main` it means "Auto modes" (Hold, Takeoff, Land, Return, Descend, Follow Target, Precland, Orbit), and bits 3 and 4 are new. The same value 7 now also ignores RC loss during Takeoff, Land and Return. The metadata diff does not flag this as a rename or a default change; only comparing the bit lists does. Max accepted the new meaning in anticipation of allowing multi-agent setups (in which requiring multiple RCs is not possible since we only have one).

### Cosmetic Changes and New Options

No action, but the **description column** in the reference was updated so it matches updated descriptions from `main`:

- Relabelled options: `BAT*_SOURCE` ("Power Module / Analog"), `COM_ARM_WO_GPS` (1 is now "Allow arming (with warning)", 2 "Allow arming (no warning)"; our 0 still means deny), `COM_FLTMODE*` ("Position / Cruise"), `COM_RC_IN_MODE` ("Joystick" is now "MAVLink"), `COM_PREARM_MODE`.
- New options: `NAV_RCL_ACT` 7, `COM_LOW_BAT_ACT` 4, `SENS_EN_SF1XX` 8 and 9, new `COM_FLTMODE*` values.
- Widened behavior: `COM_ARM_HFLT_CHK` now also covers watchdog dump files.

`COM_ARM_HFLT_CHK` is also a lesson in **keeping a workaround on purpose**. We set it to 0 because a failed USB connection blocks arming. PX4 issue [#29346](https://github.com/PX4/PX4-Autopilot/issues/29346) (hardfault of the USB MAVLink task after arming following a USB unplug) is **open at the time of writing (2026-10-22)** and, per Max, affects our board. It is filed against the Cube Orange+, and its author says it is fixed on `main` by PRs #28185 and #28197; that was not verified in source. So the parameter stays 0, and the reference links the issue so a later reader knows when to revisit it.

### New Parameters Worth a Decision

- **`GNSS_REQ_FIX`** (new, default 3). Value 6 means RTK fixed. Max chose 6: there is no reason to fly without RTK anymore ever since Max set it up to be plug-and-play. Before this, Max would just wait for RTK anyways before flying. The check fails when the reported fix type is below the setting (`gnss_checks.cpp`) and needs bit 10 of `GNSS_CHECK` (see "Renamed, but the Migrated Value Does Not Mean What You Want"). With `COM_ARM_WO_GPS` = 0, arming is denied unless the receiver reports RTK fixed. **It is a strict check, which is decisive before arming.** Once the strict checks have passed on the ground, the checks that decide while armed are the relaxed ones with fixed limits (3D fix, 50 m, 10 m/s), so losing RTK in flight does not trip it. Any offboard code the user writes should really land immediately on a fix type below 6, just like Max's offboard tests do.
- **`EKF2_SENS_EN`** (new, default 8191 = all 13 sources on). Next section.
- **`GNSS_REQ_TIME`** (new, 10 s): left at default. Not every new parameter needs a value in the template; it still has to be looked at.

### Interactions Between Your Own Decisions

This is where a human decision and the source can disagree.

**Stick override versus nudging.** Max first wanted both `MAN_OVERRIDE_SPD` at its default and `MPC_AUTO_NUDGING` = 3 (yaw and landing nudging), so that the RC could adjust yaw and landing in autonomous flight. The source says otherwise: the `MPC_AUTO_NUDGING` description requires `MAN_OVERRIDE_SPD` = -1, and `manualControlCheck()` has no exception for nudging. With both on, only slow stick movements nudge, and a fast one switches to Position mode. Max decided that **stick override is far more important**, so `MPC_AUTO_NUDGING` stays 0. The two are effectively mutually exclusive, which was not visible from the parameter names.

**`EKF2_SENS_EN` against the `*_CTRL` parameters.** Each fusion source runs only if its `EKF2_SENS_EN` bit **and** its own control parameter are both nonzero (`intended() = enabled && available`; `available` comes from `EKF2_GPS_CTRL`, `EKF2_OF_CTRL`, `EKF2_RNG_CTRL`, `EKF2_BARO_CTRL`, `EKF2_MAG_TYPE`). `EKF2_SENS_EN` is applied only while disarmed. Max's bit choices:

| Bit | Source | Set | Why |
|---:|---|:---:|---|
| 0 | GNSS 0 | 1 | The Here4. |
| 1 | GNSS 1 | 0 | There is no second GPS. |
| 2 | Optical flow | 1 | Must match `EKF2_OF_CTRL` = 1. |
| 3 | External vision | 0 | RTK is good; no mocap. |
| 4 to 7 | Aux global position 0 to 3 | 0 | None fitted. |
| 8 | Barometer | 1 | Height estimate. |
| 9 | Range finder | 1 | Must match `EKF2_RNG_CTRL` = 1 or 2. |
| 10 | Magnetometer | 1 | Critical. |
| 11 | Airspeed | 0 | Quadcopter. |
| 12 | Ranging beacon | 0 | None. |

**Max's doubt, kept on purpose.** Max was unsure how this has to match `EKF2_OF_CTRL` and `EKF2_RNG_CTRL`, and whether turning GNSS 1 off could stop the GPS from loading. The source answers the first (it is an AND), but not how it behaves on the vehicle. Being unsure is fine and expected; that is what a test flight, and an in-person check that the GPS still loads, are for. Write the doubt down in the reference, as was done here.

**A human error caught in review.** Max's first draft computed the value as 1798 from the binary string `0011100000110`. Read with bit 0 on the right, that string has bit 0 clear and bit 1 set: GNSS 0 off, GNSS 1 on, the opposite of the bit list next to it. The bits listed (0, 2, 8, 9, 10) give 1 + 4 + 256 + 512 + 1024 = **1797** = `0011100000101`. Always recompute a bitmask from the bit list and check it against the `module.yaml`/enum, not against the string.

### Things in the Old Reference That the Source Changed or Refuted

- The 1.16.2 note that `EKF2_MIN_RNG` "is expected to become the default in 1.18" was wrong about the version: it already was in 1.17.0.
- The 1.16.2 note that RTK over uXRCE-DDS is impossible "because there is no topic for it yet" was true on 1.16.2, and was exactly what PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368) changed: it added `/fmu/in/rtcm_corrections`. That PR has since been merged after the test flights succeeded, so the sentence is now out of date for `main`, and for 1.19.0 when it is released (likely).
- `BAT3_I_OVERWRITE` exists on `main` (it did not in 1.16.2).
- The new `MOTFAIL_*` descriptions on `main` still refer to the old `FD_ACT_*` names. **Upstream descriptions are not reliable either.**
- `BAT_V_OFFS_CURR` was in the 1.16.2 `.params` template but had no row and no reason in the 1.16.2 reference. It now has a row saying exactly that.

## The Calibration Parameters

[Calibration Parameters](../calibration-and-per-drone-parameters.md) lists what is unique to each drone. If a name there changed, the sensor must be recalibrated after the upgrade, because its saved value would no longer be read.

All 107 per-drone names were checked against `main`: `CAL_GYRO*`, `CAL_ACC*`, `CAL_MAG*` (offsets, scales, `ODIAG`, `ID`, `PRIO`, `ROT`), `CAL_BARO*`, `SENS_BOARD_X/Y_OFF`, `RC1` to `RC10` (`MIN`/`TRIM`/`MAX`), `BAT1_V_DIV`, `BAT1_A_PER_V`, `LND_FLIGHT_T_HI/LO`, `COM_FLIGHT_UUID`, `EKF2_MAG_DECL`. **All names exist on both 1.16.2 and `main`, with the same type and default.** The only change is that `SENS_BOARD_X/Y/Z_OFF` now have a range of ±45°, and the sample values are well inside it. No entry of [Calibration Parameters](../calibration-and-per-drone-parameters.md) needs to change for this port.

**The test flight verified that the calibration parameters survived the upgrade: seemingly all of them carried over without being ported by hand.** This is new as of the flights for PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368). One candidate addition is `SENS_GNSS0_ID` (see "Renamed, and PX4 Migrates the Value"), a new per-drone value.

## Decisions Max Made

| Question | Decision |
|---|---|
| `MAN_OVERRIDE_SPD` | Keep the default (1.0). |
| `MPC_AUTO_NUDGING` | Keep 0. Override matters more (see "Interactions Between Your Own Decisions"). |
| Removed parameters with hardcoded behavior | Accepted, after the kill-switch investigation. |
| `GNSS_REQ_FIX` | 6, require RTK fixed. `GNSS_CHECK` set to 2047 so it is enforced. |
| Renamed parameters | Ported with their values. |
| New defaults (`BAT*_V_CHARGED`, `COM_FLTT_LOW_ACT`, `FD_ACT_EN`, etc.) | Accepted. "Is Default" column updated. |
| Battery thresholds | Unchanged fractions; the 4.2 V shift is more conservative and accepted. |
| `COM_ARM_HFLT_CHK` | Keep 0, link issue [#29346](https://github.com/PX4/PX4-Autopilot/issues/29346) (open on 2026-10-22). |
| `EKF2_SENS_EN` | 1797, with the bit table above. Doubts recorded. |

## What Was Produced

- [example-parameters-px4-main.params](example-parameters-px4-main.params): 194 parameters (the 1.16.2 file had 201). Every name, type and range validated against the metadata generated from `main`. Differences from the 1.16.2 template: 13 removed outright; 13 renamed (11 carried over with their values, one with a type change, plus `GNSS_CHECK` and `MPC_AUTO_NUDGING`, which get explicit values); `GNSS_REQ_FIX`, `EKF2_SENS_EN`, `MAN_OVERRIDE_SPD` and three `MOTFAIL_*` added; and five values moved to the new defaults (`BAT1/2/3_V_CHARGED`, `COM_FLTT_LOW_ACT`, `FD_ACT_EN`).
- [Example Parameters for PX4 Main](example-parameters-for-px4-main.md): every row has its "Is Default" mark recomputed against the layered defaults of `main` (no mismatches), descriptions updated, a new GNSS section, a new MOTFAIL section, the `EKF2_SENS_EN` bit table, and a closing table of removed or renamed parameters.
- [Calibration Parameters](../calibration-and-per-drone-parameters.md): verified unchanged.

## What Was Tested, and What Is Left

- **Firmware was built and the drone flew.** The flight tests are described in PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368). Max also verified the new kill-switch logic.
- **Not recorded as verified:** that `SENS_GNSS0_OFFX/Y/Z` reach `vehicle_gnss.antenna_offset`; that the estimator reports GNSS, flow, range, baro and mag as intended with `EKF2_SENS_EN` = 1797 (`estimator_fusion_control`); that the GPS still loads with GNSS 1 off; that arming is denied below RTK fixed; that issue [#29346](https://github.com/PX4/PX4-Autopilot/issues/29346) still affects the vehicle.
- The migration-path claim (see "Renamed, and PX4 Migrates the Value") and the claims about PRs [#28185](https://github.com/PX4/PX4-Autopilot/pull/28185) and [#28197](https://github.com/PX4/PX4-Autopilot/pull/28197) are inferences or hearsay, labelled as such.
- `main` moves daily. The result is valid for commit `5f429033bf` and the PR [#29368](https://github.com/PX4/PX4-Autopilot/pull/29368) branch on 2026-10-22, and for nothing else.

## Checklist for the Next Person

1. Pin both versions as worktrees; generate `parameters.json` for each.
2. Diff names, types, defaults, ranges, enums and bit lists for every documented parameter.
3. Read the migration code and where it is called from.
4. For each removed parameter: compare your value to the new hardcoded behavior; read the consumer.
5. For each changed default: recompute everything that depends on it.
6. Diff the layered defaults (board, airframe, `rc.mc_defaults`).
7. Look at the **new** parameters in the groups you use (`GNSS_*`, `EKF2_SENS_EN` here); not every one needs a value.
8. Make the human decisions explicit and write the doubts down.
9. Validate the new template mechanically against the target's metadata.
10. Check [Calibration Parameters](../calibration-and-per-drone-parameters.md) names the same way.
11. Re-read every claim that came from a description or a release note, and either check it in code or label it unverified.
