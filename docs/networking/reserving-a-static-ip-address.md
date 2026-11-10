---
title: Reserving a Static IP Address
author: Max Gardenswartz
updated: 2026-11-06
status: active
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  How to give a device a fixed IP address, in the UniFi network console. The Autonomy Park and the Indoor Lab both have UniFi Wi-Fi systems.
---

Every device on the Autonomy Park and Indoor Lab networks should have a fixed IP address, listed on [IP Reservations](../software/ip-reservations.md). Both labs have UniFi (Ubiquiti) Wi-Fi systems, managed in the UniFi network console. On each network, the router (gateway) login portal is at `192.168.1.1`. To get access to it, see [Contacts](../start-here/contacts.md).

!!! note "Netplan Is Indoor Lab Only"
    The Autonomy Park does not use netplan files. The Indoor Lab computers also need them: see [Networking Setup (Indoor Lab)](networking-setup-indoor-lab.md).

!!! warning "Jetsons: Set the IP Before the Hostname"
    Set a Jetson's IP address before you change its hostname.

## Steps

1. Log in to the UniFi network console.
2. Go to **Client Devices**.
3. Find the device whose IP address you want to fix, and select it.
4. In the panel on the right, check **Fixed IP Address**.
5. Enter a valid local IP address that is not already reserved. UniFi will show you a warning.
6. Add the device to the reservation list for its lab, found through [IP Reservations](../software/ip-reservations.md).
