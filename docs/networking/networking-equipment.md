---
title: Networking Equipment
author: Max Gardenswartz
updated: 2026-11-10
status: draft
status_note: Copied from the Autonomy Park's UniFi device list on 2026-11-06. The physical locations are not documented yet.
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  The Autonomy Park's UniFi (Ubiquiti) switches, access points, and gateway, and how they connect. Includes how to read the UniFi device list.
---

All our networking equipment is Ubiquiti. It is managed in the UniFi network console (see [Reserving a Static IP Address](reserving-a-static-ip-address.md)).

## Autonomy Park

### How It Connects

The gateway (Dream Machine Special Edition) gets its Internet from Starlink. Everything else hangs off it, as a tree:

* **Dream Machine Special Edition** (the gateway)
    * port 1: U7 Pro Outdoor Front
    * port 4: U6 Lite Command
    * port 11: USW Pro 48 PoE (over a 10 GbE SFP+ link)
        * port 9: USW Flex Mini
        * port 11: U6 Lite Shed
        * port 48: U7 Pro Outdoor Rear

### The Devices

| Type | Name | IP Address | Plugged Into | Port | Link | 2.4 GHz Channel | 5 GHz Channel | Last Updated |
|---|---|---|---|---|---|---|---|---|
| UDM SE | Dream Machine Special Edition | `192.168.1.1` | Starlink | | GbE | | | 2026-11-06 |
| USW Pro 48 PoE | USW Pro 48 PoE | `192.168.1.69` | Dream Machine Special Edition | 11 | SFP+ (10 GbE) | | | 2026-11-06 |
| USW Flex Mini | USW Flex Mini | `192.168.1.146` | USW Pro 48 PoE | 9 | GbE | | | 2026-11-06 |
| U7 Pro Outdoor | U7 Pro Outdoor Front | `192.168.1.150` | Dream Machine Special Edition | 1 | GbE | 1 (20 MHz) | 161 (40 MHz) | 2026-11-06 |
| U7 Pro Outdoor | U7 Pro Outdoor Rear | `192.168.1.99` | USW Pro 48 PoE | 48 | GbE | 1 (20 MHz) | 157 (40 MHz) | 2026-11-06 |
| U6 Lite | U6 Lite Shed | `192.168.1.145` | USW Pro 48 PoE | 11 | GbE | 11 (20 MHz) | 40 (40 MHz) | 2026-11-06 |
| U6 Lite | U6 Lite Command | `192.168.1.48` | Dream Machine Special Edition | 4 | GbE | 6 (20 MHz) | 149 (40 MHz) | 2026-11-06 |


## Indoor Lab

The Indoor Lab's Wi-Fi networks are `NCRLab` and `NCRLab_5GHz`. Its networking equipment is:

| Type | Notes |
|---|---|
| USW Lite 19 PoE | `192.168.1.150`. A switch |
| U7 Pro | `192.168.1.18`. A Wi-Fi access point |
| Cloud Gateway Ultra | The gateway. Its IP address is *Unknown*{ .unknown }. It is not listed in the UniFi devices, so this is not confirmed |

## How to Read the UniFi Device List

* **Type:** the model of the device. The U7 Pro Outdoor and the U6 Lite are Wi-Fi access points (the Wi-Fi radios). The USW devices are switches (the USW Pro 48 PoE has 48 ports and powers the access points over Ethernet, PoE). The UDM SE is the gateway: the router, a switch, and the UniFi controller in one box.
* **Name:** the label we gave the device in UniFi.
* **Application:** the UniFi application that manages the device. All of ours say **Network**.
* **Status:** whether UniFi can reach the device. Ours say **Online**.
* **IP address:** the device's address on the network.
* **Uplink:** how the device connects upstream, and the speed of that link. **GbE** is gigabit Ethernet. **SFP+ (10 GbE)** is a 10 gigabit link through an SFP+ port.
* **Parent device:** the device it is plugged into, and the port number on that device. The tree above is the parent devices drawn out.
* **Channels (access points only):** the Wi-Fi channel and channel width each radio uses. The channel numbers 1, 6 and 11 are the 2.4 GHz radio. The larger numbers (40, 149, 157, 161) are the 5 GHz radio.
