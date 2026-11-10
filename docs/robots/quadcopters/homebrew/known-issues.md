---
title: Known Issues
author: Max Gardenswartz
updated: 2026-11-10
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  Half of the Homebrews have bad lidar cables, battery readings are voltage-only and sag, and nothing turns off a low-battery Homebrew that is not armed.
---

!!! danger "Nothing Turns Off a Low-Battery Homebrew That Is Not Armed"
    If a Homebrew is on but not armed, nothing shuts it off when the battery runs low. You are responsible for watching its battery in QGC and unplugging it, especially if debugging takes hours.

!!! danger "Half of the Homebrews Have Bad Lidar Cables"
    Half of the Homebrews' lidars were soldered with a custom cable that proved devastating to safe flight. See the [status table](#status-of-each-homebrew) below for which ones, and [Case Study: Lidar and CAN Sensor Burnout](case-studies/lidar-and-can-sensor-burnout.md).

## The Homebrew SD Cards Are Slow

The Homebrews' SD cards have a very slow write speed, at most 5 MB/s. Logging anything more than `SDLOG_PROFILE` = 1 to the SD card causes gaps in the data. Faster SD cards are expensive, so this is not planned to change.

## The Landing Gear Retracts on Landing If Plugged In

If the landing gear is plugged in, it retracts on landing. It is probably fixable, but we just unplugged it.

## Battery Readings Are Voltage-Only

The current sensor is either not soldered or not configured correctly (most likely not soldered). All battery level measurements are therefore voltage-only, and voltage sags under load. Set the battery thresholds conservatively for safety. See [Parameters](parameters.md).

## Status of Each Homebrew

There are 21 Homebrews. There is no Homebrew 01.

| Homebrew | PX4 | Ready to Fly | homebrew_docker Set Up | Lidar | Flight Controller | Crash History | Flown by Max | Sensors Calibrated | Notes | Last Updated |
|---|---|:---:|:---:|---|---|---|:---:|:---:|---|---|
| Homebrew 02 | 1.16.2 | ❌ | ❌ | Wired incorrectly; probably burned out | Bad | Has not crashed | Yes | Yes | The flight controller has USB issues, and XRCE topics run slow (94 Hz). The reason is unknown. | 2026-11-06 |
| Homebrew 03 | 1.16.2 | ✅ | ❌ | Wired incorrectly; probably burned out | None reported | Crashed before | Yes | Yes | Crashed into the net on 2026-10-09 ([why](case-studies/mavros-link-saturation.md)). | 2026-11-06 |
| Homebrew 04 | 1.16.2 | ✅ | ❌ | Wired incorrectly; probably burned out | None reported | Crashed before | Yes | Yes |  | 2026-11-06 |
| Homebrew 05 | 1.16.2 | ❌ | ❌ | Wired correctly | Bad | Crashed before | Yes | Yes | A hard fault of unknown cause on 2026-01-30 broke the GPS antenna. | 2026-11-06 |
| Homebrew 06 | 1.16.2 | ✅ | ❌ | Wired incorrectly | None reported | Has not crashed | Yes | Yes |  | 2026-11-06 |
| Homebrew 07 | 1.16.2 | ✅ | ❌ | Wired incorrectly | None reported | Has not crashed | Yes | Yes |  | 2026-11-06 |
| Homebrew 08 | 1.16.2 | ✅ | ✅ | Wired correctly | None reported | Crashed before | Yes | Yes |  | 2026-11-06 |
| Homebrew 09 | 1.16.2 | ✅ | ❌ | Wired incorrectly | None reported | Has not crashed | Yes | Yes |  | 2026-11-06 |
| Homebrew 10 | 1.16.2 | ❌ | ❌ | No lidar | None reported | Crashed before | No | Yes | The first Homebrew ever made. Brandon Fallin and Jordan Insinger crashed it before Max took over flight tests. Max has never flown it. | 2026-11-06 |
| Homebrew 11 | 1.16.2 | ✅ | ❌ | Wired incorrectly | None reported | Crashed before | Yes | Yes |  | 2026-11-06 |
| Homebrew 12 | 1.16.2 | ✅ | ❌ | No lidar | None reported | Crashed before | Yes | Yes |  | 2026-11-06 |
| Homebrew 13 | 1.16.2 | ✅ | ❌ | Wired correctly | None reported | Has not crashed | Yes | Yes |  | 2026-11-06 |
| Homebrew 14 | 1.18beta | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 15 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 16 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 17 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 18 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 19 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 20 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 21 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |
| Homebrew 22 | 1.16.2 | ❌ | ❌ | Wired correctly | None reported | Not yet flown | No | No | | 2026-11-06 |

For the shared parameters and the checks to make before flying, see [Overview](overview.md) and [Flying Manually](flying-manually.md).
