---
title: Building PX4
author: Max Gardenswartz
updated: 2026-11-03
status: draft
status_note: Written from Max's notes. The commands are the standard PX4 ones. The macOS tab has not been run by the lab.
applies_to: [apark]
assisted_by: Claude
glance: >-
  How to build PX4 firmware for the Homebrews, for any future version or to get an old one. The official guide is almost enough; this page fills the gap.
---

!!! warning "Build for the CubePilot Orange, Not the Orange+"
    The Homebrews use a CubePilot Blue H7, but the build target is the **CubePilot Orange** (`cubepilot_cubeorange_default`), not the Orange+. The Blue and the Orange run the same firmware.

This is how to make new firmware (or get an old version) for the Homebrews. Use it for every future PX4 version. To flash the latest stable release, you can use QGroundControl's **Firmware** tab instead (see [PX4 Configuration](../px4-configuration.md)).

The official guide is [Building PX4](https://docs.px4.io/v1.16/en/dev_setup/building_px4). Follow it, with the one addition below: it is missing the step that runs the install script in the `Tools` folder.

## Steps

Run these in a terminal on Ubuntu, in WSL, or on macOS. Native Windows is not supported.

1. Clone PX4 with its submodules:

    ```bash
    git clone --recursive https://github.com/PX4/PX4-Autopilot.git
    ```

2. Check out the version you want (e.g., 1.16.2) and update its submodules:

    ```bash
    cd PX4-Autopilot
    git checkout <version-tag>
    git submodule update --init --recursive
    ```

3. Install the build tools with the install script in the `Tools` folder. This is the step the official guide does not mention:

    === "Linux / WSL"

        ```bash
        bash ./Tools/setup/ubuntu.sh
        ```

        Restart your computer afterward, as the script asks.

    === "macOS"

        ```bash
        bash ./Tools/setup/macos.sh
        ```

    === "Windows"

        Building PX4 on native Windows is not supported here. Use WSL and follow the Linux / WSL tab.

4. Build for the CubePilot Orange:

    ```bash
    make cubepilot_cubeorange_default
    ```

5. The firmware is the `.px4` file in the `build/cubepilot_cubeorange_default/` folder. Flash it with QGroundControl's **Firmware** tab, as described in [PX4 Configuration](../px4-configuration.md).

## Keep the Firmware

Keep a copy of every `.px4` file you use. The one for 1.16.2 is on [PX4 Configuration](../px4-configuration.md).
