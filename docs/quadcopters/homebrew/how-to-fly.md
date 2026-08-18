---
title: Flying Manually
---

## 1.0 Safety and Legal Requirements
**Flying these drones is inherently dangerous.** Failure to follow these protocols results in personal liability for equipment damage and FAA violations.

### 1.1 Range and Legal Boundaries
* **The Net is the Limit:** Only fly inside the Autonomy Park’s net. Legally, the net is considered an "indoor" environment.
* **FAA Warning:** Flying outside the net requires an FAA license, a registered drone, and prior airspace clearance via an approved vendor. Violations can carry fines between $10,000 and $100,000.
* **Line of Sight:** The pilot must maintain a continuous line of sight with the drone at all times.

### 1.2 Personal & Bystander Safety
* **Attire:** Tie back loose hair and clothing. 
* **No Gloves:** Pilots must never wear gloves; full tactile feedback from the gimbals is required for precise control.
* **The "Live" Rule:** Never work on a drone that has a battery and propellers attached if a receiver is connected to the flight controller. Even without a transmitter powered on, rogue signals or software glitches can trigger motors.

## 2.0 Pre-Flight Preparation
### 2.1 Hardware Setup
1.  **Receiver:** Ensure the FrSky receiver is correctly wired and paired to the Taranis QX7.
2.  **GPS Fix:** **Do not power on the drone indoors and carry it outside.** The GPS EKF will initialize with poor data. Power on (or reboot via radio) only once the drone is at its takeoff position in the Park.
3.  **Battery Monitoring:** Always have a dedicated ground station operator monitoring battery voltage over the wireless telemetry link. 

### 2.2 Pilot Readiness
If you are not an experienced pilot, you must practice in a simulator first.
* **Recommended:** *Liftoff* (Steam)
* **Alternative:** *FPV FreeRider* (Steam)
* **Note:** *DRL Simulator* is not recommended due to unrealistic "out-of-the-box" physics.
* **Note:** If flying at night, ensure the Park's floodlights are active.

## 3.0 Transmitter Configuration (Taranis QX7)
The following mapping is standard for the Homebrew fleet. Refer to the diagram below for switch locations.

![Taranis QX7 Switch Guide](../images/homebrew/qx7_guide.jpg){ align="center" width="50%" }

### 3.1 Control Mapping
| Channel | Input | Function |
| :--- | :--- | :--- |
| 1 | Right Stick (X) | **Roll** |
| 2 | Right Stick (Y) | **Pitch** |
| 3 | Left Stick (Y) | **Throttle** |
| 4 | Left Stick (X) | **Yaw** |
| 5 | Switch A (SA) | **Mode Logic (Primary)** |
| 6 | Switch B (SB) | **Mode Logic (Secondary)** |
| 9 | Switch F (SF) | **Arm / Disarm** (2-Position) |
| 10 | Switch H (SH) | **Return to Launch (RTL)** |

### 3.2 PX4 Flight Mode Logic
| SA Position | SB Position | Resulting Flight Mode |
| :--- | :--- | :--- |
| **Up / Middle** | Up | **Position** (GPS Horizontal Hold) |
| **Up / Middle** | Middle | **Hold** (GPS Loiter) |
| **Up / Middle** | Down | **Land** (Automatic Descent) |
| **Down** | Up | **Altitude** (Baro/Z-axis Hold only) |
| **Down** | Middle | **Altitude** (Baro/Z-axis Hold only) |
| **Down** | Down | **Stabilized** (Full Manual / Self-Level) |

## 4.0 Flight Operations
### 4.1 Takeoff Loop (The "30-50-70" Rule)
1.  **Mode Select:** Ensure the remote is in **Stabilized Mode** (SA Down, SB Down). Never take off in Position mode.
2.  **Arm:** Flick Switch F up. (It should start down.)
3.  **Launch:** Within 5 seconds, bring the throttle to 30-50%.
4.  **Transition:** Immediately switch to **Position Mode** (SA Up) and increase throttle to ~70% (Hover). 
* *Note: Position mode assists horizontally, but it does NOT hold altitude automatically. You must still manage the throttle stick to maintain vertical height.*

### 4.2 In-Flight Conduct
* **No Acrobatics:** These are research platforms, not racing drones. No flips, rolls, or high-speed maneuvers.
* **Stay in Mode:** Do not switch flight modes mid-air. The sudden change in GPS dependency can cause instability that is difficult to recover from.
* **Remote Safety:** Never set the remote on the ground or a chair while the drone is live. The Arm switch (SF) is easily bumped by clothing.

### 4.3 Landing Procedure
1.  **Maintain Mode:** Stay in your current flight mode (Position mode is acceptable for landing).
2.  **Slow Descent:** Ease the throttle down as slowly as possible. 
3.  **The Ground Effect:** As you approach the floor, an air cushion (Ground Effect) will make the drone "float." You will need to slowly decrease throttle further to punch through this cushion for touchdown.
4.  **Disarm:** Once the landing gear makes contact, flick Switch F (SF) to the Down position. 
5.  **Safety Buffer:** Wait for the motors to come to a **complete stop** before entering the net.

**Warning:** In the current PX4 configuration, the disarm switch is not a "Kill Switch." If flipped in the air, the drone will attempt to land rather than cutting power immediately.


