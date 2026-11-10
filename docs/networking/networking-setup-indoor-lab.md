---
title: Networking Setup (Indoor Lab)
author: "Max Gardenswartz, Brandon Fallin"
updated: 2026-11-10
assisted_by: Claude
applies_to: [indoor-lab]
glance: >-
  The Indoor Lab network has no Internet, so every computer needs a special netplan file. Follow this page to set one up.
---

Everything on this page runs on a Linux computer.

Our lab's LAN is not connected to the Internet, so each computer needs a special netplan file such that all DNS traffic goes to UF but all robot traffic stays on our private LAN. Our LAN has a WiFi component. While it can be joined, this is only for robots (unless you have two WiFi cards somehow).

### Route DDS Traffic Through Robot Network

!!! note
    **Every user on the Indoor Lab computers must do this step. Otherwise your nodes will not work.**

To get all ROS traffic to be routed through the robot network, download the super client configuration file and put it in your home folder.

[Download the Indoor Lab Super Client Configuration](configs/indoor-lab-superclient-config.xml){ .md-button download="indoor-lab-superclient-config.xml" }

Do not edit the file, not even the spacing. The Autonomy Park has its own file.

[Download the Autonomy Park Super Client Configuration](configs/autonomy-park-superclient-config.xml){ .md-button download="autonomy-park-superclient-config.xml" }

Lastly, set the following environment variables in `.bashrc`
```
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export FASTRTPS_DEFAULT_PROFILES_FILE=/home/$USERNAME@ad.ufl.edu/indoor-lab-superclient-config.xml
```
Open a new terminal and run your ROS nodes without any networking issues!

### Route DNS Traffic Through UF Network

!!! warning
    **ONLY PERFORM THE FOLLOWING STEPS IF YOU ARE SETTING UP THE COMPUTER OR SOMETHING WITH THE NETWORK IS BROKEN.**

To make everything work properly, we use the following `netplan` file. Run `sudo nano /etc/netplan/01-network-manager-all.yaml` and paste the following. This example is for the computer under IP 192.168.1.202 (MAE-BPLJHL2).

You will need to know the device name for your Ethernet (used for robots/LAN) and wireless/WiFi adapater (all computers have a built-in card for it) from `ifconfig`.

Replace `enp0s31f6` with your computer's unique Ethernet interface name. `dhcp4: true` lets the Ubiquiti router dictate the IP, which should be statically assigned in the Ubiquiti portal. The Ubiquiti router also tries to serve a DNS and default gateway with this local IP, so `dhcp4-overrides` disables them.

```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp0s31f6:
      dhcp4: true
      dhcp4-overrides:
        use-routes: false
        use-dns: false
```
After saving, run `sudo netplan apply`.

### Netplan Files for the Indoor Lab Computers

| Computer | Netplan file |
|---|---|
| MAE-WD-DTG7FZ3 | [netplan-mae-wd-dtg7fz3.yaml](configs/netplan-mae-wd-dtg7fz3.yaml){ download } |
| MAE-WD-4E051A0B (192.168.1.203, also the discovery server) | [netplan-mae-wd-4e051a0b.yaml](configs/netplan-mae-wd-4e051a0b.yaml){ download } |
| MAE-BPLJHL2 (192.168.1.202) | [netplan-mae-bpljhl2.yaml](configs/netplan-mae-bpljhl2.yaml){ download } |

The Ethernet interface names in these files belong to those computers. Replace them with yours.


Log in to eduroam (or use ufgetonline's script). If logging in, select "No certificate is required" then select the domain as "ufl.edu" but be sure to still use "@ufl.edu" when typing your UF username and password.

## Add to .bashrc

```
source /opt/ros/humble/setup.sh
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DISCOVERY_SERVER=192.168.1.203:11811
export FASTRTPS_DEFAULT_PROFILES_FILE=~/indoor-lab-superclient-config.xml
```
