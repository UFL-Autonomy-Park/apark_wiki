# Jetson Orin Nano Flashing Guide

<iframe width="560" height="315" src="https://www.youtube.com/embed/-cpLgytXQ4w?si=QPlXHCRnoadTjyJ0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Required Equipment:

- **1 x NVMe SSD** (128 GB or more)
- **1 x Jetson Orin Nano Developer Kit** (Target)
- **1 x Computer** (Host) with X86 architecture, Ubuntu 22.04, and 128 GB free space
- **1 x USB-C data cable**
- **1 x Female-Female jumper wire**
- **1 x Power adapter** (included with Jetson)

## Steps:

### 1. Install SDK Manager

Download and install [**SDK Manager (SDK)**](https://developer.nvidia.com/sdk-manager) from Nvidia.  
Create a developer account if you don't have one

### 2. Insert the NVMe SSD

1. Flip the Jetson, use the longer slot to insert the SSD.
2. Insert the SSD at a 45-degree angle.
3. Press down the free end and tighten the screw to secure it.

### 3. Open SDK

Launch the SDK Manager on the host machine.

### 4. Connect Host and Target

1. Connect the host and target **directly** using the USB-C data cable.
2. Use the jumper wire to connect the GPIO pins labeled **FC REC** and **GND** (3rd and 4th flat pins from the left).
3. Connect the **target** to the **power adapter**.

!!! warning
     Connect everything **in the order listed above** and **keep the jumper wire connected**.

### 5. Configure SDK Manager (Step 1)

On the **Step 1** page of SDK Manager, select:

- **Product Category:** Jetson
- **System Configuration:**
- **Host Machine:** Ubuntu 22.04-x86
- **Target Hardware:** Jetson Orin Nano 8GB Dev Kit (**Module Number: P3767-0005**)
- **SDK Version:** **JetPack 6.0 (Rev. 2)** _(Includes CUDA version 12.2)_
- Additional SDK is optional.
!!! warning
     JetPack 6.0 is NOT automatically selected, click on the **... to select**.

### 6. Configure Installation (Step 2)

1. Navigate to **Step 2** and check everything on the page (_only Platform Service is optional_).
2. Select **Agree** and proceed to **Step 3**.

!!! warning
     The **target folder** should **not** be linked to a cloud storage.

### 7. Set Flashing Parameters

On the pop-up window, configure the following:

- **Device:** Orin Nano Dev Kit
- **OEM Config:** Pre-Config
- **User Name:** autonomypark
- **Password:** Contact admin (Brandon as of 2025)
- **Storage Device:** NVMe

### 8. Start Flashing

Click **Flash** to begin the process. The system will start downloading—**ignore the connection and disconnection messages**.

### 9. Configure Final Settings

When flashing completes, a new page will appear. Set the following:

- **Connector:** USB
- **Device:** Dev Kit
- **IP Address:** Should auto-fill. If not, use **IPv4: 192.165.55.1**
- **Credentials:** Should be copied automatically
- **Proxy Setting:** Ignore

### 10. Final Steps

1. **Unplug** the **jumper wire**.
2. Click **Install**.
3. Ensure **Dev Kit 0005** is selected and click **OK** if prompted.

### 11. Complete Installation

- Once installation completes, return to **Step 1** if you need to flash other targets.
- Otherwise, click **Finish & Exit**.

### 12. Target is Ready for Commissioning

The flashing process is complete.

### 13. Accessing the Target Ubuntu System

- Connect the Jetson to a **display and keyboard**, OR
- Use **SSH** to remotely log in.

For more details, see [this reference video](https://www.youtube.com/watch?v=q4fGac-nrTI).
