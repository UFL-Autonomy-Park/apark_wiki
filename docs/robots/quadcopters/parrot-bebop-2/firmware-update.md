---
title: Firmware Update
author: "Max Gardenswartz, Brandon Fallin"
updated: 2026-11-09
applies_to: [indoor-lab]
assisted_by: Claude
glance: >-
  For reference only: how to update a Bebop's firmware. There is no reason to update the Bebops; they all work as they are.
---

!!! danger "For Reference Only"
    There is no reason to update the Bebops' firmware. They should all work as they are. This page is provided only for reference.

## Download the Firmware

The oldest version of the Bebop firmware that is supported by SDK version 3.1.4 is firmware 4.3.1. Download this version from the [Bebop firmware folder](https://drive.google.com/drive/folders/1C0jGb8R9jWwQsnMmu70edOrFea9CGUX-?usp=sharing).

## Connect to the Bebop

If not already installed, install the Android Debug Bridge tools by running

```bash
sudo apt-get install android-tools-adb
```

Connect the Bebop to the computer using micro USB. Press the power button on the back of the Bebop once and wait for the light to become solid. Then click the power button 4 times in rapid succession. You should hear a beep. Then, run the following in the terminal to establish connection:

```bash
adb connect 192.168.43.1:9050
```

After a successful connection, the CLI should say `connected to 192.168.43.1:9050`. Now, open a Bebop shell using adb.

```bash
adb shell
```

!!! tip
    If you are **upgrading** the Bebop firmware from an older version, you do not need to modify the `dgwl.txt` file.

## Allow the Downgrade

Make the file system writable and open the whitelist of firmware versions that may be installed over the current one.

```bash
mount -o remount, rw / &&
vi /bin/updater/dgwl.txt
```

The file starts with a few comment lines, then a list of version patterns. The last two lines are:

```text
0 \ .0 \ .0
3 \ .3 \. [0-9] \ +
```

Press `i` to enter text entry mode in `vi`. Add the version number of the firmware you downloaded as a new last line:

```text
4.3.1
```

Press `ESC` to exit insert mode. Save the file and quit.

```text
:wq
```

## Install the Firmware

On an Ubuntu computer, open Files. Click "Other Locations" and in the "Enter server address..." field, type `ftp://192.168.43.1` and connect anonymously (No `username` and `password`). Rename the downloaded firmware to `bebop2_update.plf`. Copy the firmware file to `/data/ftp/internal_000` folder of the Bebop. Go back to the `adb shell` and enter

```bash
/bin/updater/updater_scan.sh /data/ftp/internal_000
```

The Bebop prints the steps of the update. It should report that the downgrade is allowed by the whitelist, and then that it is sending the file to the Update partition.

Finally, reboot the Bebop by entering `reboot` in the `adb shell`. The Bebop will reboot multiple times for the firmware upgrade.

