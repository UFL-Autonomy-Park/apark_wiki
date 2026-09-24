# Updating Here4 GNSS Firmware

This guide walks through the **only reliable method** we found for updating firmware on a CubePilot Here4 RTK GNSS module (CAN node) when your flight controller normally runs **PX4**.

**Read this whole document once before starting.** The process is safe and repeatable if followed exactly, but skipping or reordering steps can leave the Here4 in an unusable (though recoverable) state.

## Why this process is necessary

- **You cannot use QGroundControl (QGC) to flash Here4 firmware. Period.** QGC has no reliable CAN-node firmware-push tool for this device.
- PX4 does support flashing CAN peripherals directly via an SD card ([official PX4 docs](https://docs.px4.io/v1.16/en/dronecan/#firmware-directories)) — but **in practice, this gets the Here4 stuck mid-update**. It is not unrecoverable, but it will leave your GPS non-functional until you complete the procedure below.
- Mission Planner (the tool that *does* reliably flash this device) is built around ArduPilot, not PX4. Its DroneCAN detection does not work reliably against a PX4 flight controller — even with a known-good, freshly-purchased Here4 unit.
- The practical fix: **temporarily flash ArduPilot onto your flight controller**, use Mission Planner to update the Here4, then **flash PX4 back**. The Here4's firmware lives entirely on its own separate microcontroller — flashing ArduPilot onto your flight controller does not touch the Here4 at all, it just changes who's "talking" to it on the CAN bus.
- This tutorial may be relevant if the RTK setup you are using isn't working as expected.

## Requirements

- A **Windows computer**. Mission Planner is stated to also work on Linux/Android, but in our testing it fails to connect on Linux even after the commonly suggested `sudo apt install mono-complete` fix. **Don't waste your time on Linux — use Windows.**
- [Mission Planner](https://ardupilot.org/planner/) installed.
- [QGroundControl](http://qgroundcontrol.com/) installed (you already have this for normal PX4 operation).
- A CubePilot Blue flight controller (standard Cube carrier board).
- A microUSB cable.
- **The quadcopter's battery must NOT be connected for the entire process below.** Everything is powered via USB only.

Throughout this guide, **"reboot"** means: unplug the microUSB cable, wait a few seconds, then plug it back in. Do not connect the battery at any point during this procedure unless explicitly told to.

---

## Step 0: Back up your PX4 parameters

Before touching anything, export your current PX4 parameter file from QGC (**Vehicle Setup → Parameters → Tools → Save to file**). You'll need to reconfigure PX4's DroneCAN/GPS parameters from scratch after this process (ArduPilot and PX4 use completely separate parameter systems — nothing carries over automatically), and having your old values on hand makes that faster.

---

## Step 1: Check your wiring

The Here4 connects to the flight controller over CAN using a **3-wire (white/green/blue) cable** — plug this into **CAN 1** on the CubePilot Blue.

**Ignore the red and black cable entirely.** Leave it unplugged from everything for this whole process.

---

## Step 2: Flash ArduPilot onto the flight controller

Using QGC (while still connected to the quad as normal, over USB or your telemetry link):

1. Go to the firmware flashing screen and select **ArduCopter**. The latest stable version is fine.
2. Let it flash and reboot as prompted.

Your flight controller is now running ArduPilot instead of PX4. This is temporary — you'll flash PX4 back in the final step.

---

## Step 3: Set the required ArduPilot CAN/GPS parameters

**Physical state at this point:** quad powered via microUSB only, no battery connected, Here4 wired to CAN1 as in Step 1.

1. Open Mission Planner and connect **over USB** (not radio/telemetry) — click **Connect** in the **upper-right corner**.
2. In the parameter list, set the following:

   | Parameter | Value |
   |---|---|
   | `CAN_D1_PROTOCOL` | `1` |
   | `CAN_D2_PROTOCOL` | `1` |
   | `CAN_P1_DRIVER` | `1` |
   | `CAN_P2_DRIVER` | `1` |
   | `GPS_TYPE` | `9` |
   | `NTF_LED_TYPES` | `231` |
   | `CAN_D1_UC_OPTION` | `1` |

   **`CAN_D1_UC_OPTION` is the critical, easy-to-miss step.** The official Here4 manual ([docs.cubepilot.org](https://docs.cubepilot.org/here-4/here-4-manual)) does not mention it, but without it, the Here4 will not appear in Step 4 below.

3. Click **Write Params**.
4. **Reboot** the quad (unplug/replug the microUSB cable).
5. Reconnect in Mission Planner and **double-check every parameter above stuck**. Mission Planner's parameter display is not always trustworthy immediately after a write — verify by reading them back after the reboot, not just trusting the write confirmation.

**Important:** After this reboot, `CAN_D1_UC_OPTION` will read back as `0` again. **This is expected and correct** — it means the CAN register did its job of resetting so ArduPilot can now see the Here4. Do not "fix" this back to `1`; leave it as the post-reboot value shows.

---

## Step 4: Confirm the Here4 is detected

**Physical state:** unchanged from Step 3 (USB only, no battery).

1. In Mission Planner, go to **Setup → Optional Hardware → DroneCAN/UAVCAN**.
2. Select the entry corresponding to **CAN1**. The Here4 manual calls this `MAVLinkCAN1`, but as of September 2026 Mission Planner has renamed this option — look for whichever entry corresponds to CAN1 rather than matching the exact old name.
3. Click **Connect** — **not** the Connect button in the upper-right corner. This is a separate button in the **top-middle of the DroneCAN/UAVCAN screen itself.**

You should now see three entries appear:
- `org.missionplanner`
- `org.ardupilot0`
- `org.com.cubepilot.here4`

**If you only see `org.missionplanner` and nothing else, stop and troubleshoot before proceeding** — this means the Here4 isn't visible on the bus yet. Common causes: still running PX4 (Step 2 wasn't completed/saved), `CAN_D1_UC_OPTION` wasn't set before the reboot in Step 3, or a wiring issue from Step 1.

---

## Step 5: Get the correct firmware file

1. Go to **[github.com/CubePilot/GNSSPeriph-release/releases](https://github.com/CubePilot/GNSSPeriph-release/releases)**.
2. Download the **latest STABLE release** — do **not** pick a pre-release.
3. From that release, download the **`.bin`** file. Ignore any `.apj` or `.elf` files if present in the release assets — `.bin` is the correct format for flashing this CAN peripheral (`.apj` is used for flight-controller firmware, and `.elf` is a debug-symbols build for use with a hardware debug probe — neither applies here).

---

## Step 6: Flash the Here4

1. Back in Mission Planner's DroneCAN/UAVCAN screen (Step 4), find the `org.com.cubepilot.here4` entry.
2. Click **Menu → Update**.
3. When asked whether to search the internet for the latest firmware, **click No.** In our testing, this internet search can return a mismatched or even older version specifically for the Here4 — always supply the file you downloaded directly from CubePilot's GitHub in Step 5 instead.
4. When prompted, browse to and select the `.bin` file you downloaded.
5. Let it run. **Do not unplug the USB cable or interrupt this process.**

### Reading the Here4's LED during this step

This isn't documented well anywhere else, so pay attention to the LED on the Here4 itself while it updates:

- **Slowly pulsing white** — normal. The update is in progress; let it finish.
- **Solid (steady, non-pulsing) white** — this may indicate the update has failed or the unit is stuck in a bad state. If you see solid white rather than a pulse, stop and don't keep power-cycling repeatedly hoping it resolves on its own.

If the update genuinely stalls (no LED change, no progress) for an extended period — more than roughly 10 minutes with zero change — treat it as stuck rather than "still working," and move to the fallback below rather than continuing to wait indefinitely.

---

## Step 7: Verify the update succeeded

After Mission Planner reports the update as complete:

1. In the DroneCAN/UAVCAN screen, refresh/reconnect and confirm the Here4's reported firmware version now matches the release you selected in Step 5.
2. Confirm the LED has settled to its normal steady/breathing state (not pulsing, not solid white).

---

## Step 8: Return to PX4

The Here4 is now updated and independent of whatever the flight controller runs — but your quad still needs to fly on PX4.

1. In QGC, flash PX4 back onto the flight controller (whatever version you were running before — we used v1.16.2).
2. **Let the flight controller boot on PX4's own default parameters first — do not immediately load your saved `.params` file from Step 0.** Reflashing firmware families back and forth can leave the parameter set in an inconsistent state if you load a saved file over it too quickly. Let PX4 come up clean once, then load your saved parameters as a deliberate, separate step afterward.
3. **Re-set/verify your PX4 DroneCAN/GPS parameters.** These do not carry over from ArduPilot. At minimum, revisit:
   - `UAVCAN_ENABLE`
   - `UAVCAN_SUB_GPS`
   - `UAVCAN_PUB_RTCM` (if using RTK corrections)
   - `EKF2_GPS_CTRL`

   Use your Step 0 backup as a reference for the values you had before.
4. Confirm PX4 detects the Here4 again: open the MAVLink Console and run `uavcan status` — the Here4's node should show up with mode `OPERAT`.

### ⚠️ Double-check your parameters actually loaded correctly

**Do not trust a loaded `.params` file blindly — verify it, parameter by parameter, before you fly.** In our case, after loading our saved parameters back in, several `CA_` (control allocation / motor mixer) parameters silently came back wrong — for example, a value that should have been `0.25` loaded as `1.00` instead. We didn't catch this immediately, and it made the quad unflyable (the motor mixer was effectively miscalibrated). There was no obvious error or warning — the parameter file simply didn't apply cleanly across the reflash. Spot-check your critical parameters (especially anything under `CA_`) against your Step 0 backup after loading, rather than assuming the load succeeded just because it didn't throw an error.

### Recalibrate your sensors before flying

After all of the above, **recalibrate the compass** — this is required, not optional, after this process. In our case, one indoor calibration attempt wasn't enough to clear the errors; we had to calibrate the compass a second time **outdoors** before it stuck cleanly. If you see persistent compass-related errors after an indoor calibration, don't assume something else is broken — try again outside first.

For good measure, we also recalibrated **Level Horizon, the accelerometer, and the gyroscope** (i.e., all onboard sensors) at the same time, rather than just the compass alone. After doing all of this, the quad flew normally.

**Only once you've verified your parameters, recalibrated all sensors, and confirmed a healthy GPS fix should you consider reconnecting the battery and proceeding to normal flight testing. You can put the GPS back on the CAN extender rather than CAN1.**

---

## Fallback: if Mission Planner still won't cooperate

If you hit a wall anywhere in the above — Mission Planner won't detect anything even after correctly following every step, or the Here4 ends up in the solid-white stuck state — the more robust (but slightly more involved) option is to bypass Mission Planner entirely:

1. Buy a **USB-to-CAN adapter** (an adapter running "slcan" firmware, such as a CANable-style adapter, is a common and inexpensive choice).
2. Wire the adapter's CAN-H/CAN-L leads directly onto the CAN bus, in parallel with the existing Here4-to-flight-controller wiring (CAN is a shared bus, so tapping in alongside the existing connection is fine).
3. Install and run **[`dronecan_gui_tool`](https://github.com/DroneCAN/gui_tool)** (free, cross-platform) pointed at that adapter.
4. Flash the same **`.bin`** file from Step 5 through this tool instead of Mission Planner.

This talks to the CAN bus directly at the protocol level, with no dependency on either Mission Planner's or QGC's flakier CAN-over-MAVLink bridging — it's the method a PX4 core developer has used to resolve this exact class of issue in the past.
