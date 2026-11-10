---
title: Connecting to WiFi
author: "Max Gardenswartz, Jordan Insinger"
updated: 2026-11-10
applies_to: [indoor-lab]
assisted_by: Claude
glance: >-
  For reference only: working Bebops are already on the Indoor Lab LAN. This tutorial sets a Bebop's Wi-Fi network and static IP address.
---

Everything on this page runs on a Linux computer.

!!! danger "For Reference Only"
    All working Bebops should already be connected to the Indoor Lab LAN. This tutorial is provided only for reference. Do not follow it unless a Bebop has lost its network settings.

> Configure the network and IP on Bebop 2 drones and make changes persistent by adding them to the boot sequence.

---

## Step 1: Clone GitHub Repository and Edit `shortpress_3.sh`

---

### Clone the Repository

```bash
git clone https://github.com/tnaegeli/multiple_bebops.git
```

---

### Navigate to the Cloned Directory

```bash
cd multiple_bebops
```

---

### Edit `shortpress_3.sh` to Set SSID, Password, and Static IP

- Open `shortpress_3.sh` in a text editor.
- Modify the following variables. The Indoor Lab Wi-Fi name (SSID) is `NCRLab` (the 5 GHz network is `NCRLab_5GHz`). For the password, see [Contacts](../../../start-here/contacts.md).

  ```
  SSID: 'NCRLab'
  PW: 'Unknown'
  IP: 192.168.1.1XX
  ```

- The IP must be in the correct range—refer to [IP Reservations](../../../software/ip-reservations.md).
- After configuring, **add the new IP** to the reservations list.

---

## Step 2: Connect to the Bebop Using Android Debug Bridge (ADB)

---

### Install `adb` (If Not Installed)

```bash
sudo apt-get install android-tools-adb
```

---

### Connect `adb` to the Bebop

- Connect the Bebop to your computer via USB.
- Power on the Bebop and wait for the LED to remain solid.
- Press the power button **four times** until you hear the beeping sound.
- Then run:

```bash
adb connect 192.168.43.1:9050
```

- A successful message should read:  
  `connected to 192.168.43.1:9050`

---

## Step 3: Run Script and Add to Boot

---

### Run the File Copy Script

```bash
./copy_files.sh
```

---

### Open a Shell on the Bebop

```bash
adb shell
```

---

### Edit the Boot File Using `vim`

```bash
vi /etc/init.d/rcS
```

To write to file, using vim type __I__ to enter insert mode. 
To save and exit vim press __escape__ to exit insert mode, then __:wq__ to write to file and exit.

---

### Add This Line to the End of the `rcS` File Just Above the `exit 0` Line.

```bash
./bin/onoffbutton/shortpress_3.sh
```

---

### Run `ifconfig`
Run the following code in the shell
```
ifconfig eth0 192.168.1.1XX netmask 255.255.255.0 up
```
where `1XX` is your desired IP.

---

### Exit the `adb` Shell
You're in a shell within a shell. Type
```
exit
```
to get back to bash.

### Disconnect and Reboot the Bebop

```bash
adb disconnect
```

Unplug the USB and restart the drone.

---

### Assign Static IP to Bebop


Now,the Bebop will show up on the TP-Link portal. Once the Bebop connects, log into the router and assign the IP reservation for the desired address under Advanced -> DHCP Server. **Don't forget to add the IP to the Google Sheet! (see [IP Reservations](../../../software/ip-reservations.md))**

---

## Notes

- Ensure **all Bebop IPs are unique** and in the reserved range.
- If `adb` isn't working, confirm the drone is powered on and connected via USB.
- If you encounter file system permission issues, remount the filesystem as writable:

```bash
adb shell mount -o remount,rw /
```
ADB tends to not actually disconnect from devices even after running `adb disconnect`. You can force a disconnect using: `adb kill-server`.

