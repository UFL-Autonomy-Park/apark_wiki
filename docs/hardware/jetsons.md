---
title: Jetsons
author: "Max Gardenswartz, Wyatt Cross, Willie Warke"
updated: 2026-11-10
status: draft
status_note: Not a complete inventory. No one has counted the Jetsons yet. Only the Jetsons with reserved IP addresses are listed.
applies_to: [apark]
assisted_by: Claude
glance: >-
  What the Jetsons are, how to use one that is already set up, and how to flash a new Jetson Orin Nano with JetPack 6.0 rev 2. The full count and labels are still to be done.
---

A Jetson lets a robot run high-compute autonomous programs on board, instead of relying only on its low-power computer for low-level control (for example, a flight controller). Each Jetson is a full computer that runs Ubuntu. The Ubuntu release cannot be upgraded the normal way, because it is bundled in a JetPack version. We currently use JetPack 6.0 rev 2 (see [Software We Use](../software/software-we-use.md)).

!!! note "No Wheels for Python JAX"
    The Jetsons do not have prebuilt wheels for Python's `jax` library.

## How Many Are There

* **Jetson Orin Nanos:** about 30. Most are set up, but they are not all labeled, and no one has counted them. Most of these are for the Homebrews.
* **Orin NX units:** the lab also has some. They have not been inventoried.
* **Which model every other Jetson is:** *Unknown*{ .unknown }.

## Use a Jetson That Is Already Set Up

Most Jetsons are already flashed. To use one, connect it to Ethernet and SSH in, finding its IP address on the Client Devices page of the UniFi gateway. Or connect a keyboard, mouse, and monitor. The Jetsons' IP addresses are on [IP Reservations](../software/ip-reservations.md).

A Jetson in the Indoor Lab needs Ethernet with Internet access, or its Wi-Fi changed, to download anything: the Indoor Lab network has no Internet. See [Networking Setup (Indoor Lab)](../networking/networking-setup-indoor-lab.md).

To pull logs and speed up debugging on a Jetson with an AI agent, see [AI for Debugging Jetsons](../software/ai-for-debugging-jetsons.md).

For a reference video on booting a Jetson from an SSD instead of an SD card, see [this video](https://www.youtube.com/watch?v=q4fGac-nrTI).

## Flash a New Jetson Orin Nano

This flashes a Jetson Orin Nano with JetPack 6.0 rev 2 from a host computer, and installs it on an NVMe SSD.

<iframe width="560" height="315" src="https://www.youtube.com/embed/-cpLgytXQ4w?si=QPlXHCRnoadTjyJ0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### What You Need

- **1 x NVMe SSD** (128 GB or more)
- **1 x Jetson Orin Nano Developer Kit** (the target)
- **1 x Computer** (the host) with X86 architecture, Ubuntu 22.04, and 128 GB free space
- **1 x USB-C data cable**
- **1 x Female-Female jumper wire**
- **1 x Power adapter** (included with the Jetson)

### Install SDK Manager

On the host, download and install [SDK Manager](https://developer.nvidia.com/sdk-manager) from NVIDIA. Create a developer account if you do not have one. Then launch it.

### Insert the NVMe SSD

1. Flip the Jetson, and use the longer slot to insert the SSD.
2. Insert the SSD at a 45-degree angle.
3. Press down the free end and tighten the screw to secure it.

### Connect the Host and the Target

1. Connect the host and target **directly** using the USB-C data cable.
2. Use the jumper wire to connect the GPIO pins labeled **FC REC** and **GND** (3rd and 4th flat pins from the left).
3. Connect the target to the power adapter.

!!! warning "Connect in This Order"
    Connect everything in the order listed above, and keep the jumper wire connected until the final steps.

### Choose What to Install (SDK Manager Step 1)

On **Step 1** of SDK Manager, select:

- **Product Category:** Jetson
- **Host Machine:** Ubuntu 22.04-x86
- **Target Hardware:** Jetson Orin Nano 8GB Dev Kit (**Module Number: P3767-0005**)
- **SDK Version:** **JetPack 6.0 (Rev. 2)** (includes CUDA 12.2)
- **Additional SDKs:** optional

!!! warning "JetPack 6.0 Is Not Selected Automatically"
    Click on the **... to select** to choose JetPack 6.0.

### Accept the Components (SDK Manager Step 2)

1. On **Step 2**, check everything on the page. Only Platform Service is optional.
2. Select **Agree** and proceed to **Step 3**.

!!! warning "No Cloud Storage"
    The target folder should not be linked to cloud storage.

### Set the Flashing Parameters

In the pop-up window, set:

- **Device:** Orin Nano Dev Kit
- **OEM Config:** Pre-Config
- **User Name:** autonomypark
- **Password:** the lab managers on [Contacts](../start-here/contacts.md) can give it to you
- **Storage Device:** NVMe

### Flash

Click **Flash**. The system starts downloading. Ignore the connection and disconnection messages.

### Finish the Installation

When flashing completes, a new page appears. Set:

- **Connector:** USB
- **Device:** Dev Kit
- **IP Address:** it should fill in automatically. If not, use **IPv4: 192.165.55.1**
- **Credentials:** they should be copied automatically
- **Proxy Setting:** ignore

Then:

1. Unplug the jumper wire.
2. Click **Install**.
3. Make sure **Dev Kit 0005** is selected, and click **OK** if prompted.
4. When the installation completes, return to **Step 1** if you need to flash other targets. Otherwise click **Finish & Exit**.

The Jetson is now ready for commissioning. To log in, connect it to a display and keyboard, or use SSH.

### Troubleshooting

#### Set the IP Before the Hostname

Jetsons are finicky. Set the Jetson's IP address **before** you change its hostname. At the Autonomy Park, see [Reserving a Static IP Address](../networking/reserving-a-static-ip-address.md).

#### The apt Sources Are Messed Up

If `apt update` fails because the sources are messed up, run this on the Jetson:

```bash
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/cache/app-info
sudo apt clean
sudo apt update
```
