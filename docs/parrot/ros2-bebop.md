---
title: ROS 2 Bebop Autonomy (Driver Support)
---

# ROS 2 Bebop Driver Support

To get the Bebops to work on ROS 2, we need a driver to work with the Parrot SDK. Thankfully, [jeremyfix](https://github.com/jeremyfix) (tell him thank you) did the heavy lifting. First, we need to update the Bebop's firmware to be compatible with the SDK.

The GitHub repo for the `ros2_bebop_driver` can be found [here](https://github.com/jeremyfix/ros2_bebop_driver?tab=readme-ov-file). The GitHub repo for the `ros2_parrot_arsdk` can be found [here](https://github.com/jeremyfix/ros2_parrot_arsdk).

## Firmware Update

The oldest version of the Bebop firmware that is supported by SDK version 3.1.4 is firmware 4.3.1. Download this version of the firmware [here](https://github-wiki-see.page/m/uavpal/beboptwo4g/wiki/Manual-firmware-upgrade-and-downgrade-of-Parrot-Bebop-2).

!!! note
	If the GitHub repos or Bebop firmware files are no longer available, they are backed up on our NAS. Reach out to the admin for more information.

If not already installed, instal the Android Debug Bridge tools by running

```
sudo apt-get install android-tools-adb
```

Connnect the Bebop to the computer using micro USB. Press the power button on the back of the Bebop once anf wait for the light to become solid. Then click the power button 4 times in rapid succession. You should hear a beep. Then, run the following in the terminal to establish connection:

```
adb connect 192.168.43.1:9050
```

After a successful connection, the CLI should say `connected to 192.168.43.1:9050`. Now, open a Bebop shell using adb.

```
adb shell
```

!!! tip
    If you are **upgrading** the Bebop firmware from an older version, you do not need to modify the `dgwl.txt` file.

Run the following command

```
mount -o remount, rw / &&
vi /bin/updater/dgwl.txt
```

You should see the contents of the file `dgwl.txt`:

```
# List of firmware versions to which to downgrade is allowed
# Regexps are basic regular expressions (BRE). See grep (1) manpage on a
# linux desktop to get the correct syntax (especially metacharacters escapes).
0 \ .0 \ .0
3 \ .3 \. [0-9] \ +
```

Press `i` to enter text entry mode in `vi`. Type the version number of the firmware you downloaded in the last line:

```
# List of firmware versions to which to downgrade is allowed
# Regexps are basic regular expressions (BRE). See grep (1) manpage on a
# linux desktop to get the correct syntax (especially metacharacters escapes).
0 \ .0 \ .0
3 \ .3 \. [0-9] \ +
4.3.1
```

Hit `ESC` to exit the insert mode. Save the file by typing

```
:wq
```

Hit `ENTER`. On an Ubuntu computer, open Files. Click "Other Locations" and in the "Enter server address..." field, type `ftp://192.168.43.1` and connect anonymously (No `username` and `password`). Rename the downloaded firmware to `bebop2_update.plf`. Copy the firmware file to `/data/ftp/internal_000` folder of the Bebop. Go back to the `adb shell` and enter

```
/bin/updater/updater_scan.sh /data/ftp/internal_000
```

The Bebop should return the following:

```
[FIRMWARE UPDATER] Boot # 4: Scanning / data / ftp / internal_000 for updates ...
[FIRMWARE UPDATER] Boot # 4: searching PLF named files * .plf ...
[FIRMWARE UPDATER] Boot # 4: Testing /data/ftp/internal_000/bebop2_update.plf
[FIRMWARE UPDATER] Boot # 4: Checking the downgrading whitelist /bin/updater/dgwl.txt ...
[FIRMWARE UPDATER] Boot # 4: whitelist: # List of firmware versions to which to downgrade is allowed
# Regexps are basic regular expressions (BRE). See grep (1) manpage on a
# linux desktop to get the correct syntax (especially metacharacters escapes).
0 \ .0 \ .0
3 \ .3 \. [0-9] \ +
4.3.1
[FIRMWARE UPDATER] Boot # 4: search result: 4.3.1
[FIRMWARE UPDATER] Boot # 4: downgrading allowed by whitelist
[FIRMWARE UPDATER] Boot # 4: Sending
/data/ftp/internal_000/bebop2_update.plf to the Update partition
[FIRMWARE UPDATER] Boot # 4: Move command is <mv>
```

Finally, reboot the Bebop by entering `reboot` in the `adb shell`. The Bebop will reboot multiple times for the firmware upgrade.

## Network Connection

Follow the directions in the [Configuring the WiFi on Bebops](../parrot/configure-network.md) guide. 
## Install Driver

First, create a new workspace:

```
mkdir bebop_ws
cd bebop_ws
```

Install the following dependencies

```
sudo apt install ros-humble-camera-info-manager libavdevice-dev && sudo apt install libavahi-client-dev

```

Run the command to make sure that it does not hang on install

```
git config --global color.ui auto
```

Now install the `ros2_parrot_arsdk`

```
git clone https://github.com/jeremyfix/ros2_parrot_arsdk src/ros2_parrot_arsdk
colcon build --packages-select ros2_parrot_arsdk
```

The build should take around 2 to 3 minutes. If this fails to build quickly, it happens to be due to the repo command waiting for a reply on enabling color display. I'm not sure how to bypass that question, you can try

```
cd bebop_ws/src/ros2_parrot_arsdk
mkdir build
cd build
cmake ..
make
```

Next, run

```
git clone https://github.com/jeremyfix/ros2_bebop_driver.git src/ros2_bebop_driver
colcon build --symlink-install
source install/setup.bash
git clone https://github.com/jeremyfix/ros2_parrot_arsdk.git src/ros2_parrot_arsdk
colcon build --symlink-install
```

After this, you should be able to run the launch file

```
source bebop_ws/install/setup.bash
ros2 launch ros2_bebop_driver bebop_node_launch.xml ip:=YOUR.BEBOP.IP.ADDRESS
```
