# Radio and RC Setup Guide
**Version 1.0 (October 11, 2025)**

This document serves as the official guide to the radio control systems used for the lab's Homebrew drone fleet. Its purpose is twofold: first, to document our current legacy hardware setup for operation and troubleshooting; second, to provide a clear and definitive upgrade path for all future builds.

The RC hobby has undergone significant, and often confusing, technological shifts. Adhering to the procedures and recommendations in this guide will prevent the compatibility issues and time-consuming troubleshooting that have historically plagued this field.

---
## 1. Current Lab Standard Configuration
This table details the components of our primary drone control system as of the date above.

| Component              | Manufacturer & Model / Software Name         | Version & Comments                                                                                             |
| ---------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Transmitter (Hardware)** | FrSky Taranis X9D Plus (non-2019 model)      | This is our legacy radio. Note that batteries and chargers are no longer produced, marking it as end-of-life.   |
| **Transmitter (OS)** | OpenTX                                       | v2.3.15. This is the final version of OpenTX; the project is no longer in development.                           |
| **Internal TX Module** | FrSky XJT                                    | ACCST D16 v2.1.0 (FCC). This firmware is on the internal radio module, separate from OpenTX.                      |
| **Receiver** | FrSky X8R                                    | ACCST D16 v2.1.0 (FCC). Must match the transmitter module's protocol, version, and region (FCC).                   |
| **Flight Controller (FC)** | CubePilot Blue                               | Communicates with the receiver via the S.BUS protocol.                                                         |
| **FC Firmware** | PX4 Autopilot                                | v1.16 (or latest stable release). Our standard autopilot software stack.¹                                      |
| **Ground Control Station** | QGroundControl                               | Used for flight planning, parameter configuration, and real-time monitoring, or configuring the FC via a microUSB cable.                                   |

¹<small>Note: The CubePilot Blue hardware is often associated with ArduPilot, as it’s written on the side of it. We use PX4 only, so don’t let this decal mislead you. ArduPilot isn’t a part of the CubePilot Blue’s model name.</small>

---
## 2. Glossary of Essential RC Terminology
**Transmitter (TX)**: The handheld radio controller used by the pilot. It converts stick and switch movements into a digital radio signal. Also called a "radio."

**Receiver (RX)**: A small component on the drone that receives the signal from the transmitter and sends the commands to the Flight Controller.

**Binding**: The process of creating a unique, exclusive digital link between one transmitter and one receiver. A bound receiver will only respond to its paired transmitter.

**Flight Controller (FC)**: The "brain" of the drone. It takes input from the receiver and sensors (gyros, accelerometers, GPS) to stabilize the aircraft and execute commands.

**Firmware**: Low-level software that runs on hardware. In our context, this refers to the software on the radio modules (like the XJT's ACCST firmware) and the receiver, which is separate from the transmitter's main operating system (OpenTX).

**FrSky**: A manufacturer of RC hardware that was once the de facto standard but now represents a legacy ecosystem due to their transition to a modern product line that is expensive and runs entirely proprietary software.

**Taranis**: A popular series of transmitters made by FrSky, including our lab's X9D Plus model.

**XJT**: The name of the internal transmitter module inside the Taranis X9D Plus.

**OpenTX**: The powerful, open-source operating system that runs on Taranis transmitters. Its development is now defunct, with the last version being 2.3.15.

**Protocol**: The "language" used for wireless communication between the transmitter module and the receiver. Examples include ACCST, ACCESS, and ELRS.

**Serial Communication Protocol**: The language used for the wired communication between the receiver and the flight controller.

**PPM (Pulse Position Modulation)**: An older, aggregate signal format that encodes multiple PWM channels into a single, analog-style pulse train. While it allows for a single-wire connection between the receiver and flight controller, it suffers from high latency and low resolution compared to modern digital protocols. It is now considered obsolete for performance-oriented drones.

**S.BUS (Serial Bus)**: A digital communication protocol originally developed by Futaba and widely adopted by FrSky. It transmits up to 16 channels of control data from the receiver to the flight controller over a single wire. It is a reliable, one-way protocol for control input only; a separate protocol like S.Port is required for telemetry. It is not deprecated yet, as of October 2025, but is being superseded in modern systems.

**FPort (FrSky Port Protocol)**: A newer, more efficient protocol from FrSky designed to be the successor to the S.BUS and S.Port combination. FPort is a bidirectional protocol that cleverly combines RC control data and telemetry into a single data stream on one wire, simplifying wiring significantly.

**IBUS (FlySky Bus)**: The serial communication protocol used by the manufacturer FlySky. Functionally, it is FlySky's direct equivalent to S.BUS, providing digital channel data from the receiver to the flight controller over a single wire. A separate connection is typically required for telemetry data.

**CRSF (Crossfire Protocol)**: A high-speed, bidirectional protocol developed by Team BlackSheep (TBS) and now used as the standard for ExpressLRS (ELRS). It is renowned for its extremely low latency and high update rates. It natively carries both RC control data and extensive telemetry data in a single packet, making it the current performance standard.

**SRXL2 (Spektrum Remote Receiver Link v2)**: The modern, bidirectional serial protocol from Spektrum. It sends control data, telemetry, VTX control, and ESC data over a single wire. It is a significant improvement over Spektrum's older satellite receiver protocols (DSMX), offering faster speeds and more robust data transmission.

**S.Port (Smart Port)**: A bidirectional digital communication protocol developed by FrSky. Its primary purpose is to connect telemetry sensors (like GPS, voltage, or current sensors) in a daisy-chain configuration, allowing data from all connected sensors to be sent back to the receiver over a single wire. It is also the physical port used to flash firmware onto FrSky receivers, as described in this guide. It should not be confused with S.BUS, which is used to send control channel data *from* the receiver *to* the flight controller.

**CRSF (Crossfire)**: A modern, high-speed, bidirectional protocol developed by TBS. It is used by ELRS and other modern systems to send channel data to the FC and receive telemetry data back. This is the successor to S.BUS for all new builds.

**Telemetry**: Data sent back from the drone's receiver to the transmitter, such as battery voltage or signal strength (RSSI). This data can be displayed on the transmitter's screen or used to trigger audible alerts.

**Mode 2**: The standard stick configuration in the US. The left stick controls throttle (up/down) and yaw (left/right). The right stick controls pitch (up/down) and roll (left/right).

---
## 3. The Legacy System & The Path to Obsolescence
Our current FrSky-based system was once the gold standard. However, a series of business and technical decisions by FrSky has rendered the entire ecosystem obsolete. It is critical to understand this history to appreciate why we must transition away from it.

### The Fracture of the FrSky Ecosystem
Around 2019, FrSky made changes that created widespread chaos:

- **ACCST v1 vs. v2**: FrSky released an ACCST v2 firmware update. This update was not backward-compatible with v1. This means a v2 transmitter cannot bind to a v1 receiver, and vice versa. This created a huge burden on users to ensure every component was on the correct, matching version.
- **The ACCESS Protocol**: FrSky then introduced a new, completely locked-down protocol called ACCESS. This move was intended to block competitors and force users into a new, proprietary ecosystem, alienating much of the community.
- **Regional Firmware (FCC vs. LBT)**: To comply with regulations, all protocols also come in two regional flavors: FCC (for the US and most of the world) and LBT (for the EU). These are also incompatible with each other.

This leaves users with a confusing matrix of protocol, version, and region that must all match perfectly to achieve a successful bind.

### Why We Must Upgrade
Our Taranis X9D Plus and X8R system is now a dead end for several practical reasons:

- **End-of-Life Software**: OpenTX development is frozen. It will receive no new features or bug fixes.
- **Hardware Scarcity**: FrSky no longer produces batteries or chargers for the Taranis X9D Plus. Once our current hardware fails, it will be difficult and expensive to replace.
- **Poor Documentation**: FrSky's official website ([https://www.frsky-rc.com/](https://www.frsky-rc.com/)) is the only source for firmware but is **impossible to find with a search engine** and the documentation is terse, sometimes illegible, and imprecise. (Do not use retail sites like ([https://www.frskyna.com/](https://www.frskyna.com/)) for official files).
- **Cost**: New FrSky transmitters are significantly more expensive than modern, superior alternatives.

For all these reasons, while we will maintain our current setup, any hardware failure or new drone project will mandate a switch to the modern standard.

---
## 4. The Modern Standard & Recommended Upgrade Path
The RC community has moved to a fully open-source, higher-performance ecosystem. This is the required standard for all new lab purchases.

**GUI Software**: EdgeTX: The community-led successor to OpenTX. It is actively developed and supports modern hardware.
**Protocol**: ExpressLRS (ELRS): This is the new open standard for RC links. It offers vastly superior range, lower latency, and more features than any FrSky protocol.

### Recommended Hardware:
- **Transmitter**: RadioMaster TX16S or RadioMaster Boxer, with an internal ELRS module. These offer superior features to the Taranis for a fraction of the cost of new FrSky gear. A budget of under $300 is sufficient.
- **Receiver**:
    - **For PWM Output**: The RadioMaster ER8 2.4GHz ELRS PWM Receiver is a direct, modern replacement for the FrSky X8R, offering 8 physical servo ports.
    - **For Serial Connection**: For builds that only require a digital connection to the FC (most of our builds), a smaller receiver like the RadioMaster RP4TD ExpressLRS is excellent but requires soldering.
    - Always choose the FCC version when purchasing.

These components use the CRSF serial protocol to communicate with the flight controller, which is supported by our CubePilot Blue and PX4.

---
## 5. Procedures for the Current System (FrSky Taranis X9D+)
This section covers the essential procedures for operating our legacy FrSky equipment. 
> **WARNING**: ALWAYS REMOVE PROPELLERS FROM THE DRONE BEFORE PERFORMING ANY SETUP, BINDING, OR FIRMWARE UPDATES.

### 5.1 Flashing Firmware on the X8R Receiver
Firmware for the internal XJT module and the X8R receiver must match (ACCST D16 v2.1.0 FCC). You can flash the receiver directly from the Taranis.

**Required:**
- A 3-wire servo cable or 3 appropriately colored Dupont cables.
- The correct receiver firmware `.frk` file downloaded from [https://www.frsky-rc.com/](https://www.frsky-rc.com/) and placed on the transmitter's SD card in the `[FIRMWARE]` folder.

**Procedure:**
1. Power everything off. Ensure the receiver is disconnected from the flight controller.
2. Connect the servo cable to the receiver's S.Port (not S.BUS or any PWM channel).
3. Connect the other end of the servo cable to the pins in the external module bay on the back of the Taranis. Ensure the signal, power, and ground pins are correctly oriented.
4. Turn on the Taranis transmitter.
5. Long-press the MENU button to access Radio Setup. Press PAGE to navigate to the SD-HC CARD screen.
6. Navigate to the `[FIRMWARE]` folder and select the correct X8R firmware file.
7. Long-press the ENT button. A context menu will appear.
8. Select "Flash external module." The flashing process will begin. Do not disconnect power.
9. Once the "Flashing successful" message appears, you can power everything down and disconnect the cable.

### 5.2 Binding the X8R to the Taranis
1. Power everything off. 
2. Physically disconnect the receiver from the flight controller.
3. Turn on the Taranis transmitter. Use the PAGE button to navigate to the MODEL SETUP screen for your drone.
4. Scroll down to the "Internal RF" section.
5. Set Mode to `D16`.
6. Set Receiver No. to a unique number for this model (e.g., 01).
7. Select the `[Bind]` option and press ENT. Select “CH 1-8 Telemetry [ON]” or a similar option. Telemetry is not mandatory, though. The transmitter will start chirping, indicating it is in bind mode.
8. Connect the LiPo battery to the drone. Wait a few seconds for it to boot up.
9. On the X8R receiver, press and hold the F/S (Failsafe) button. You will need a pen or screwdriver to reach it.
10. While still holding the F/S button, connect the 3-pin cable to the S.BUS slots (not the massive array of PWM slots) on the receiver. Connect the other end RC slot on the CubePilot Blue flight controller. The receiver's two LEDs will light up: solid red and solid green. After a moment or two, the green LED should start flashing, indicating a successful bind. The red will still be solid. You can now release the F/S button.
11. On the transmitter, press EXIT to stop the binding process.
12. Power cycle the drone by disconnecting and reconnecting the LiPo battery (or by disconnecting and reconnecting the cable between it and the flight controller).
13. The receiver should now show a solid green LED, indicating a successful and active link.
14. You may now power off the transmitter and drone in any order. If Telemetry was enabled, the transmitter will warn you a receiver is still connected before powering off if you are powering it off first.

### 5.3 Initial Setup in OpenTX & PX4
- **Model Profiles**: In OpenTX, each aircraft has its own "model" profile. This profile stores all settings, including switch assignments, trims, and which receiver number it's bound to. Switching models in OpenTX makes the transmitter look for a different receiver; it does not unbind the previous one. Note: Model profiles cannot be directly transferred between different transmitter models (e.g., Taranis to RadioMaster) or even between different Taranis models running the same OpenTX version due to hardware differences.
- **Switches**: To use a switch, it must be configured in three places in OpenTX: HARDWARE, MIXER, and OUTPUTS.
- **Sounds**: Audio files for alerts are stored on the SD card in the `[SOUNDS]` folder. These can be assigned to switch positions or events in the SPECIAL FUNCTIONS menu. You may consider adding your own if the built-in one are imprecise for your needs. The author’s favorite is the [Open-TX-Portal-Voice-Pack](https://github.com/jarethmt/Open-TX-Portal-Voice-Pack).
- **PX4 Flight Modes**: In QGroundControl, under Vehicle Setup > Flight Modes, you will assign switches to flight modes. The required modes for our operations are:
    - **Stabilized**: Manual roll/pitch/yaw rate control, with auto-leveling. Throttle is manual.
    - **Attitude**: Manual roll/pitch/yaw angle control. More intuitive than Stabilized. Throttle is manual.
    - **Position**: The drone holds its position (latitude, longitude, altitude) using GPS when sticks are centered.
    - **Hold**: The drone will stop and hold its current position.
    - **Land**: The drone will automatically land at its current position.
- **Safety Features**:
    - **Arm/Disarm**: Assign a switch in PX4 to arm and disarm the motors. This is a critical safety function.
    - **Failsafe**: The receiver failsafe must be set to ensure the drone does not fly away if the signal is lost. For PX4, the failsafe should be set to "No Pulses" on the receiver. [PDF for setting X8R failsafe](#)
    - **Return Mode**: DO NOT USE the default "Return to Land" or "Return to Launch" mode on the drone. Our operational areas often have obstacles that make this unsafe. The designated failsafe action is either Land or Hold.

---
## 6. Frequently Asked Questions (FAQ)
**Q: My receiver has a solid green light, but QGroundControl shows no stick/switch inputs?**
**A:** This is almost always a wiring issue. The X8R must be connected to the flight controller via the single S.BUS port, not the main block of PWM channel pins. Ensure the 3-wire cable runs from the X8R's S.BUS port to the correct RC Input port on the CubePilot.

**Q: I switched models on my Taranis and the drone disconnected. Is it unbound?**
**A:** No. The receiver remains bound to the transmitter's internal module. OpenTX model profiles are associated with a "Receiver No." When you switch models, the transmitter starts trying to talk to a different receiver number. Simply switch back to the correct model profile to reconnect.

**Q: Do I need a 16-channel receiver to get 16 channels to the flight controller?**
**A:** No. The number in a receiver's name (e.g., ER8) typically refers to the number of physical PWM (servo) outputs. A digital serial protocol like S.BUS or CRSF sends all 16 channels over a single wire to the flight controller, regardless of how many PWM ports the receiver has.

**Q: What do I do if I sever a receiver antenna?**
**A:** Never solder a severed antenna. This will alter its length and impedance, leading to unpredictable signal loss and potential flyaways that are impossible to debug. Replace the antenna with an identical part. If a replacement is not available, replace the entire receiver. It is not worth the risk.

---
## 7. Resources and Procurement
### Recommended Vendors:
- [GetFPV.com](https://GetFPV.com): Excellent selection and the best return/damage policy.
- [RaceDayQuads.com](https://RaceDayQuads.com) (RDQ): Fast shipping, great for smaller components.
- [Amazon.com](https://Amazon.com): Good for generic supplies but verify sellers for specialized hardware.

## 8. Disclaimer & Final Recommendations
This guide is a living document intended to serve as a **starting point** for operating and upgrading the lab's RC equipment. While every effort has been made to ensure accuracy, the RC hobby is complex, and legacy hardware, in particular, is prone to unique and unforeseen failures.

Treat this document as a reference, not an infallible set of instructions. During the creation of this guide, for example, the Taranis X9D+'s internal SD card failed without warning and a new one had to be procured. **Expect the unexpected**, and always be prepared to troubleshoot.

If you encounter an issue not covered here, or if a procedure does not yield the expected result, it is crucial to cross-reference information with other resources. Consulting modern **YouTube tutorials**, searching **Google Images** for correct wiring diagrams, or asking an **AI assistant** for clarification can often provide the solution that this document may lack.

## 9. Learning Resources
For general drone building and hardware reviews, the author recommends Joshua Bardwell on YouTube as a highly respected and knowledgeable source.

## 10. A Note on Procurement
To the best of our knowledge, nearly all hobbyist RC hardware is manufactured in China. Be aware that university and grant funding may have restrictions on purchasing electronics from these sources. Plan accordingly.