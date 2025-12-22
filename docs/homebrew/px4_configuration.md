---
title: PX4 Configuration, Parameters, and Firmware
---

# PX4 Firmware & Parameter Deployment: Homebrew Fleet

## 1.0 Firmware Versioning Logic
PX4 does not provide a porting tool for parameters between versions. Major (1.x to 2.x) and minor (x.15 to x.16) updates often involve opaque changes to parameter names and EKF logic. 

* **Standard Practice:** Users are expected to reconfigure PX4 from scratch when a new minor/major version is released.
* **Legacy Data:** If you update firmware from a previous version, PX4 will attempt to keep as many parameters as possible. This is **undesirable** and leads to errors.
* **Deltas:** The script `compare_px4_params.py` was used to identify differences between a working 1.15.4 set and a default 1.16.0 set to create our current template. Use this as a baseline for future upgrades (e.g., 1.16 to 1.17).

## 2.0 Connection Protocols
### 2.1 Wired (USB)
Use for flashing firmware, configuring the **Actuators** tab, and high-speed data transfer.
* **Safety:** Start with the drone **disconnected from the battery** and **all propellers removed**. Connect to the computer via USB (directly to the Flight Controller or the spare dongle).

### 2.2 Wireless (Radio)
Use for sensor calibration and general telemetry. 
* **Baud Rate:** Ensure the baud rate is set to **57600**. If QGC shows a default, leave it at this value.
* **Limitation:** The **Actuators** tab is inaccessible via radio; it will revert to the legacy **Motors** tab. Do not modify settings here.
* **Linux Permission:** If dialout permissions fail, run `sudo usermod -a -G dialout $USER`, then **restart** the machine.

### 2.3 Manual Connection Discovery
If autoconnect fails, identify the port and set permissions:
* **macOS:** `ls /dev/cu.*` followed by `sudo chmod 666 /dev/cu.[ID]`. You may see something like `/dev/cu.usbserial-B0048D22`. Skipping this results in a "Permission error when locking device" message.
* **Linux:** `ls /dev/tty*`
* **Windows (PowerShell):** Run `Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'USB' }` to identify the COM port. Use port `XXXXX`.
* **Note on Adapters:** USB-C adapters/docks generally do not cause issues unless it is the first time use and the driver is still installing.

## 3.0 Clean Configuration Procedure
Perform these steps via USB with **no propellers** and **no battery** connected.
1.  **Reset:** In the **Parameters** tab, select **Reset all to firmware defaults**.
2.  **Reboot:** Use the **Reboot Vehicle** button in QGC.
3.  **Airframe:** Select **Generic Quadcopter (Quad X)**. Ignore the red sensor errors in the log for now.
4.  **Reboot:** Again.
5.  **ESC Calibration:** Follow the QGC wizard. Ensure propellers are removed before plugging in the battery when prompted.
6.  **Power:** Calibrate battery voltage using a physical voltmeter for reference.
7.  **Template:** Load the `homebrew_1_16_0.params` file. Ignore all legacy versions.
8.  **Reboot:** Final reboot to commit parameter changes.

## 4.0 Sensor Calibration
Disconnect USB and switch to wireless radio to prevent cable snags and connector damage during movement. Seal the drone up for a firm grip.
1.  **Orientation:** In the **Sensors** tab, set `SENS_BOARD_ROT` to **Yaw 90 deg** (Raw Value: 2). The Homebrew FCs are mounted 90° clockwise from the desired front-facing side.
2.  **Required Calibrations:** Level Horizon, Accelerometer, Gyroscope, and Compass.
3.  **Critical Warning:** You **must** recalibrate every drone individually. Loading a `.params` file imports the specific calibration offsets of the source drone. Because every drone has unique magnetic interference (soft/hard iron) and IMU biases, using another drone's calibration will cause measurements to drift or trigger EKF failures.

## 5.0 Critical Technical Notes
### 5.1 Firmware Management
The PX4 repository does not maintain easily accessible binaries for older releases. When you flash via QGC, it pulls the **latest stable** version automatically. 
* **Internal Storage:** We maintain the stable binary `cubepilot_cubeorange_default_1_16_0.px4` to avoid forced upgrades. 
* **Source Building:** Do not attempt to build old versions from source unless you are prepared to manually roll back all recursive submodules, which is historically difficult.

### 5.2 Parameters vs. Calibrations
Not everything is stored in a `.params` file. Calibration data (like ESC calibration) is specific to the hardware-level timing and must be performed on every drone individually after a firmware upgrade, even if using a template.

### 5.3 Sensor Safety
Never calibrate sensors over USB. Compass calibration requires continuous slow spinning. USB cables will snag, tangle, and potentially damage the flight controller port or the cable itself. Use the wireless radio.