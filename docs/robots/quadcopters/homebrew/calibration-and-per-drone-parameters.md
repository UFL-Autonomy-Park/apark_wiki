---
title: Calibration and Per-Drone Parameters
author: "Max Gardenswartz"
updated: 2026-10-21
assisted_by: Claude
applies_to: [apark]
glance: >-
  The PX4 parameters that are unique to each Homebrew and never copied between drones. Read it so you know what parameters should differ between drones.
---

!!! warning "Read Parameters in the PX4 v1.16 Reference Only"
    To understand any parameter on this page, use the [PX4 v1.16 parameter reference](https://docs.px4.io/v1.16/en/advanced_config/parameter_reference). Do not use the main (latest) reference: parameters differ between PX4 versions.

--8<-- "qx7-personal-note.md"

Reference: PX4 **v1.16** (`release/1.16`). Values in the "Sample" column come from one sample drone. "Default" is the v1.16 source default.

These parameters are **not** part of the first-time setup checklist in [PX4 Configuration](px4-configuration.md). They are unique to each physical drone (sensor and battery calibrations, device IDs) or written by the firmware itself (see the last section). After a full parameter wipe or a firmware upgrade, redo the calibrations below on every drone. Do not copy another drone's values. Parameter names may change between firmware versions, so re-check the names against the new release.

## Unique to Each Drone: Redo on Every Quadcopter

### Gyroscope (`CAL_GYRO*`)

Each quadcopter needs its own gyroscope calibration. The firmware also relearns and saves gyro offsets by itself over time, so these values drift slightly from boot to boot.

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `CAL_GYRO0_XOFF` / `YOFF` / `ZOFF` | −0.001093 / −0.004653 / 0.025502 | 0 | Each quadcopter needs its own gyroscope calibration. |
| `CAL_GYRO1_XOFF` / `YOFF` / `ZOFF` | 0.017696 / −0.007145 / 0.004775 | 0 | Same. |
| `CAL_GYRO2_XOFF` / `YOFF` / `ZOFF` | 0.034279 / 0.000794 / 0.000492 | 0 | Same. |

### Accelerometer (`CAL_ACC*`)

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `CAL_ACC0_XOFF` / `YOFF` / `ZOFF`, `XSCALE` / `YSCALE` / `ZSCALE` | 0.134527 / 0.047541 / 0.039388, scales 1 / 1 / 1 | 0 offsets, 1 scales | Each quadcopter needs its own accelerometer calibration. |
| `CAL_ACC1_*` (same six) | 0.273077 / −0.156760 / −0.185613, scales 1.002418 / 1.000138 / 0.988593 | 0 offsets, 1 scales | Same. |
| `CAL_ACC2_*` (same six) | −0.024469 / 0.267408 / 0.261582, scales 1.003901 / 0.999136 / 0.987734 | 0 offsets, 1 scales | Same. |

### Compass (`CAL_MAG*`)

Calibration slots are matched to sensors by device ID (`CAL_MAG*_ID`), so the same compass can sit in a different slot on a different drone.

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `CAL_MAG0_XOFF` / `YOFF` / `ZOFF`, `XSCALE` / `YSCALE` / `ZSCALE` | 0.103816 / −0.113710 / 0.023709, scales 1.024196 / 0.997193 / 0.974344 | 0 offsets, 1 scales | Each quadcopter needs its own compass calibration. |
| `CAL_MAG1_*` (offsets, scales and `XODIAG` / `YODIAG` / `ZODIAG`) | 0.123004 / −0.029632 / 0.013106, scales 0.972365 / 1.071113 / 0.946423, odiag −0.022899 / 0.006623 / 0.001966 | 0 offsets, 1 scales, 0 odiag | Same. |

### Barometer (`CAL_BARO*_OFF`)

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `CAL_BARO1_OFF` | 87.328125 | 0 | Written by the firmware for this specific sensor. Not copied between drones. |

### Level Flight (`SENS_BOARD_X_OFF`, `SENS_BOARD_Y_OFF`)

These are the parameters QGC's Level Horizon (Level Flight) calibration writes. In the PX4 source, `level_calibration.cpp` updates exactly these two: roll offset to `SENS_BOARD_X_OFF` and pitch offset to `SENS_BOARD_Y_OFF`, in degrees. `SENS_BOARD_Z_OFF` (yaw) is not touched by that calibration and stays 0.

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `SENS_BOARD_X_OFF` | −2.0350902° | 0 | Each quadcopter needs its own Level Flight calibration. |
| `SENS_BOARD_Y_OFF` | −0.3200225° | 0 | Same. |

### RC Calibration (`RC1` to `RC10`)

Max manually calibrated the RC to trim away stick drift for his personal Taranis QX7. Defaults are 1000 (min), 1500 (trim), 2000 (max).

| Parameter Name | Sample (MIN / TRIM / MAX) | Default | Reason |
|---|---|---|---|
| `RC1_MIN` / `RC1_TRIM` / `RC1_MAX` | 982 / 1492 / 2006 | 1000 / 1500 / 2000 | Manually calibrated RC to trim away stick drift. |
| `RC2_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC3_*` | 982 / 982 / 2006 | 1000 / 1500 / 2000 | Same. (Throttle trim sits at minimum.) |
| `RC4_*` | 982 / 1497 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC5_*` | 1150 / 1578 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC6_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC7_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC8_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC9_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |
| `RC10_*` | 982 / 1494 / 2006 | 1000 / 1500 / 2000 | Same. |

### Battery Sensing (`BAT1_V_DIV`, `BAT1_A_PER_V`)

Each quadcopter needs its own battery voltage-divider and current-per-volt calibration. In v1.16 the metadata default for both is −1, which means "use the board default"; the Cube Orange board defaults are 10.1 and 17. The other battery parameters are in [Homebrew Parameters](parameters.md).

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `BAT1_V_DIV` | 12.05901 | −1 (uses the Cube Orange board default, 10.1) | Found by a unique calibration for each quadcopter. |
| `BAT1_A_PER_V` | 6.940631 | −1 (uses the Cube Orange board default, 17) | Found by a unique calibration for each quadcopter. |

### Sensor Device IDs and Priorities (`CAL_*_ID`, `CAL_*_PRIO`, `CAL_MAG0_ROT`)

Each calibration slot above is tied to a sensor through its device ID. The ID encodes the bus type, bus, address and device type, so the same sensor can land in a different slot on a different drone. Sample IDs are from one drone; treat them as per-drone values and do not copy them. Which of these the firmware writes automatically when it detects or calibrates a sensor has not been verified in the source.

| Parameter Name | Sample | Default | Reason |
|---|---|---|---|
| `CAL_ACC0_ID` / `CAL_ACC1_ID` / `CAL_ACC2_ID` | 3670050 / 2621474 / 2424842 | 0 | Device IDs of the three accelerometers. Per drone. |
| `CAL_ACC0_PRIO` / `CAL_ACC1_PRIO` / `CAL_ACC2_PRIO` | 50 / 50 / 50 | −1 (uninitialized) | 50 is "Medium (Default)" in the parameter enum. |
| `CAL_GYRO0_ID` / `CAL_GYRO1_ID` / `CAL_GYRO2_ID` | 3670050 / 2621474 / 2424842 | 0 | Device IDs of the three gyroscopes. Per drone. |
| `CAL_GYRO0_PRIO` / `CAL_GYRO1_PRIO` / `CAL_GYRO2_PRIO` | 50 / 50 / 50 | −1 (uninitialized) | Same. |
| `CAL_MAG0_ID` / `CAL_MAG1_ID` | 8944643 / 589858 | 0 | Device IDs of the two compasses. Per drone. |
| `CAL_MAG0_PRIO` / `CAL_MAG1_PRIO` | 75 / 0 | −1 (uninitialized) | 75 is "High" and 0 is "Disabled" in the parameter enum. |
| `CAL_MAG0_ROT` | 0 | −1 (Internal) | 0 is "No rotation" in the parameter enum. `CAL_MAG1_ROT` was at the default (−1). |
| `CAL_BARO0_ID` / `CAL_BARO1_ID` | 3997730 / 3997706 | 0 | Device IDs of the two barometers. Per drone. |
| `CAL_BARO0_PRIO` / `CAL_BARO1_PRIO` | 50 / 50 | −1 (uninitialized) | Same as the accelerometers. |

## Written by the Firmware: Do Not Set

These are written by PX4 itself while it runs. Do not set them by hand and do not copy them from another drone. They are listed so that a full parameter comparison does not flag them as mistakes. In the v1.16 source, the QGC "reset all" task and the boot-time reset both keep `LND_FLIGHT_T_HI`, `LND_FLIGHT_T_LO` and `COM_FLIGHT_UUID`; `EKF2_MAG_DECL` is not excluded and returns to its default.

| Parameter Name | Sample | Default | What writes it |
|---|---|---|---|
| `LND_FLIGHT_T_HI` / `LND_FLIGHT_T_LO` | 1 / 795910513 | 0 / 0 | Total flight time of this autopilot in microseconds, `(HI << 32) \| LO`. Written by the land detector (`LandDetector.cpp`). Unique to each quadcopter. |
| `COM_FLIGHT_UUID` | 25 | 0 | Number of the next flight, incremented automatically on every disarm. Written by the commander (`Commander.cpp`). Unique to each quadcopter. |
| `EKF2_MAG_DECL` | −6.299414° | 0 | Magnetic declination. The estimator stores the declination it learns when it differs from the stored value by more than 0.1° (`EKF2.cpp`), so it changes with where in the world the drone is flown. |
