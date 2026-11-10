---
title: "Case Study: Position Mode Instability"
author: Max Gardenswartz
updated: 2026-11-03
status: active
status_note: Written from flight notes, not from log analysis. The root cause of the Homebrew 05 hard fault is still unknown.
applies_to: [apark]
assisted_by: Claude
glance: >-
  In early 2026, Max was test flying all new Homebrews as they were built. 50% of Homebrews flew well in Stabilized mode but twitched, drifted, or crashed in Position mode randomly and intermittently (every third flight or every 10 minutes of flight time). This is what was tried and what changed after the 1.16.2 upgrade with lidar and optical flow enabled.
---

## The Pattern

Flight tests on 2026-01-16 and the months before on PX4 1.16.0 showed two kinds of Homebrew:

* "Perfect drones": When flying in Position Mode, Homebrews 02, 07, and 09 held position with no movement when the sticks were centered (expected behavior), and also handled well in Stabilized mode. They were certified as ready for future autonomy experiments.
* Homebrews that handled well in Stabilized mode but not in Position mode: Homebrew 04 twitched and crashed randomly one day, breaking the landing gear. Homebrew 08, 11 and 12 drifted, wandered up to 2 m, or twitched and crashed randomly one day.

Stabilized mode was always fine on every Homebrew, so the problem was in the position estimate or the position controller, not in the motors or the airframe.

## What Was Tried

| Date | Homebrew | What was tried | Result |
|---|---|---|---|
| 2026-01-23 | 05 | Set `EKF2_MULTI_IMU` to 1 from the usual 3. | Position mode still performed badly. |
| 2026-01-23 | 12 | Reflashed the whole OS and rewrote all parameters. | Perfect hover for 2 to 3 minutes, then aggressive drift and low-frequency oscillation, then a violent twitch that forced a crash landing from about 2 m. |
| 2026-01-30 | 05 | Flew repeatedly, with and without restarting. | About every fourth flight was perfect. A front flip in Position mode broke the GPS antenna; the cause was a hard fault of unknown origin. |
| 2026-01-30 | 08 | Flew in Position mode with a bad fix. | Twitched and crashed after 12 seconds. |
| 2026-02-06 | 11 | Tested the vibration hypothesis: remounted the canopy so it does not touch the flight controller, then recalibrated all sensors. | Stabilized was fine. Altitude mode could not hold altitude, and Position mode could not hold position. It twitched a few seconds in and broke a landing gear while about 1 m off the ground. |

On Homebrew 11, the PX4 log suggested a lidar problem: the lidar measurement was never used for anything. Vibration remained a concern. The task that followed was to replace the lidar.

Homebrew 03 and 06 on 2026-02-06 gave more clues. Neither climbed when flown over a hill, which suggests the height estimate was relying on the barometer only. Both also showed "height estimate unstable" errors on some (but not all) boots, and Homebrew 03 reported the distance sensor's bottom-valid flag as always 0.

## What Changed

On 2026-05-01 the fleet moved to PX4 1.16.2, and the parameters were changed to enable the lidar and optical flow (EKF2_RNG_CTRL=1 and EKF2_OF_CTRL=1). Earlier flights had been made without them enabled. Max simply wasn't aware of these sensors since he was new to these quadcopters.

After that, Homebrew 05, 08, and 13 flew as expected and were certified. Homebrew 13 flew three flights each in Stabilized, Altitude and Position modes, all as expected. No issues like the "twitching" and whatnot were ever experienced again.

## Lessons

* A Homebrew that is perfect in Stabilized can still be bad in Position. Stabilized should be reserved for experience pilots but is a good debugging tool.
* If not using RTK, GPS is not sufficient for stable flying on the Homebrews. It is, however, on the Astros presumably since the Astros have the benefit of a company-backed design and more expensivee sensors.
* When the above test flights were run, no RTK corrections were used. With RTK, optical flow and lidar are actually *not* required and even make handling slightly worse. Max now recommends keeping them off. However, your offboard code must land if RTK fix falls below 6 (full fix) since there are no longer fallbacks! If flying manually, monitor QGC carefully for RTK faults (e.g., falling back to 5). Falling back from 6 (fix) to 5 (float) is **not expected except after a crash**.
* Intermittent faults (perfect every fourth flight) are hard to debug. Save the log for each flight.

## Related

* [Known Issues](../known-issues.md#status-of-each-homebrew)
* [Case Study: Lidar and CAN Sensor Burnout](lidar-and-can-sensor-burnout.md)
