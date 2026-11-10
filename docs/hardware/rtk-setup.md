---
title: RTK Setup
author: Max Gardenswartz
updated: 2026-11-10
applies_to: [apark]
assisted_by: Claude
glance: >-
  RTK corrections come from our Emlid Reach RS3 ground station. Ground robots with an Emlid unit get them over LoRa radio; all other robots get them from the RTKLib caster, never the RS3's embedded caster.
---

--8<-- "rtk-intro.md"

## Ground Station

Our ground station is an Emlid Reach RS3. It is configured from the Emlid Flow mobile app.

![An Emlid Reach RS3 GNSS receiver beside its black carrying case, a USB cable, and an antenna.](../images/facilities/emlid-reach-rs3.jpg){ width="50%" }

*The Emlid Reach RS3 (product image).*

The ground station is mounted at the Autonomy Park **main shed** (not the storage shed), on the mounting tower seen in the video below.

### Setting Up

Follow the instructions in the video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/5HQKhlVAA2k?si=d-zeR1WPQD1aoatq" title="Emlid GPS base station startup" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

The Emlid is battery powered, and the battery lasts about 24 hours. To charge while using it, plug a USB-C charger into the surge protector in the equipment cabinet next to the mounting tower.

!!! danger "Do Not Break the Equipment Cabinet's Lock"
    The cabinet requires a key, but the key has been lost. Take the smallest pliers from the toolbox in the main shed and carefully open the cabinet by twisting each of the key slots. Spread the pliers' jaws apart (do not twist the center part).

    If you break this piece, all the equipment in the cabinet (for example, the barometer) is no longer weatherproof and will be damaged.

### Before You Leave

1. Power off the Emlid **before** unmounting it.
2. Unmount it.
3. Put it away in the Emlid RS3's case, with the mounting screw and the LoRa antenna. Do not lose either one.
4. Close the equipment cabinet.
5. Take the Emlid inside the main shed before you leave.

Never take the Emlid off the premises of the Autonomy Park.

## Emlid Flow Settings for Ground Station

Get the Emlid Flow app for your phone.

[Emlid Flow on the App Store](https://apps.apple.com/us/app/emlid-flow/id1463967138){ .md-button target="_blank" }
[Emlid Flow on Google Play](https://play.google.com/store/apps/details?id=com.emlid.reachview3){ .md-button target="_blank" }

!!! note " Single Is Expected for the Ground Station"
    The fix status in the upper right of the Emlid Flow app shows **Single** for the ground station. That is expected, because the ground station has no corrections to receive. It is not expected for the rovers: a rover should not stay on Single once it is receiving corrections.

The receiver is named `TOWERBASESTATION` in the Emlid Flow app, and joins the `UFLAutonomyPark` Wi-Fi network. You will not be able to 5 GHz network; that's okay. These are its base settings.

| Setting | Value |
|---|---|
| Base output 1 | TCP server, `localhost:9000` |
| Base output 2 | LoRa radio, 920.0 MHz, 18.23 kb/s |
| Correction format | RTCM3 |
| RTCM3 message 1006 (base position) | 0.1 Hz |
| RTCM3 messages 1074, 1084, 1094, 1230 (GPS, GLONASS, Galileo, GLONASS biases) | 1 Hz |
| RTCM3 message 1124 (BeiDou) | Off |
| Coordinates entry method | Manual |
| Base marker | 29.62840700° N, -82.36057600° E, ellipsoidal height 0.849 m |
| Antenna height | 2.174 m |

The screenshots below are the same settings in the app.

<div class="grid cards" markdown>

![Emlid Flow Receivers screen showing the receiver, its Wi-Fi network, and the base outputs.](../images/facilities/emlid-flow-home.jpg){ width="60%" }

![Emlid Flow settings screen.](../images/facilities/emlid-flow-settings.jpg){ width="60%" }

![Base output 1 set to TCP server on localhost port 9000.](../images/facilities/emlid-flow-base-output-1.jpg){ width="60%" }

![Base output 2 set to LoRa radio at 920.0 MHz.](../images/facilities/emlid-flow-base-output-2.jpg){ width="60%" }

![RTCM3 messages and their rates.](../images/facilities/emlid-flow-rtcm3.jpg){ width="60%" }

![Base settings with manual coordinates and antenna height.](../images/facilities/emlid-flow-base-settings.jpg){ width="60%" }

</div>

* **Our Emlid units:** four rover units labelled Emlid RS 001 to 004, and one RS3, which is the ground station. All four rovers are RS+ units, and they are configured identically.

## Emlid Flow Settings for Rovers/Clients

These are the settings of one of the rover Emlid RS+ units in the Emlid Flow app. All four (RS+) are configured identically. While any could be used as a base station, we use them on robots as recipients of RTK corrections ("rovers"). 

| Setting | Value |
|---|---|
| Correction input | LoRa radio, 920.0 MHz, 18.23 kb/s (shows "Receiving corrections") |
| Wi-Fi | `UFLAutonomyPark` |
| Base output 1 and 2 | Off |
| Position streaming 1 | Serial, USB to PC, 57600, NMEA |
| Position streaming 2 | TCP server, `localhost:9001`, NMEA |

<div class="grid cards" markdown>

![Emlid Flow Receivers screen showing the connected rover Emlid RS 002, an RS+, with its correction input and Wi-Fi network, and the TowerBaseStation RS3 listed as available.](../images/facilities/emlid-rover-home.jpg){ width="60%" }

![The rover's Correction input screen with LoRa radio selected at 920.0 MHz and receiving corrections.](../images/facilities/emlid-rover-correction-input.jpg){ width="60%" }

![The rover's Settings screen listing Base output 2, Bluetooth, GNSS settings, and position streaming.](../images/facilities/emlid-rover-settings.jpg){ width="60%" }

![Position streaming 1 set to Serial, USB to PC, 57600, NMEA.](../images/facilities/emlid-rover-position-streaming-1.jpg){ width="60%" }

![Position streaming 2 set to TCP server on localhost port 9001, NMEA.](../images/facilities/emlid-rover-position-streaming-2.jpg){ width="60%" }

</div>

## How Corrections Reach the Robots

![A diagram of two paths from the Emlid RS3 ground station: LoRa radio directly to a ground robot, and over the local network to the RTKLib caster on the discovery server and then to an NTRIP client on a quadcopter's Jetson, through MAVROS to the flight controller and over UAVCAN to the GPS.](../images/facilities/rtk-overview.svg){ width="80%" }

*How RTK corrections reach ground robots (LoRa) and quadcopters (local NTRIP and a caster).*

There are two ways, depending on the robot:

* **Ground robots with an Emlid unit (for example, an RS)** use LoRa radio.
* **All other robots** use the RTKLib caster. This includes the quadcopters.

This dual system was not chosen because Wi-Fi or the caster would get saturated with many agents (that is not known). It was chosen to minimize changes to existing configurations.

### The RTKLib Caster

Corrections are served by RTKLib running on the discovery server computer. An NTRIP client on each quadcopter's companion computer publishes them to `<mavros_namespace>/mavros/gps_rtk/send_rtcm`. Serving RTK through QGC does not work: see [PX4 Configuration](../robots/quadcopters/homebrew/px4-configuration.md).

**Use the RTKLib caster, never the RS3's embedded caster.**

The caster is already running. For how it was built, see [NTRIP Caster for RTK on Quadcopters](../networking/ntrip-caster-for-rtk-on-quadcopters.md) (reference only).

* **RTKLib version:** 2.4.3. It is very stable and has not needed an update since 2020.
* **RTKLib configuration:** the access details for getting corrections from the RTKLib caster are in the `homebrew_docker` repository. They are not published on the wiki. See [GitHub Access](../start-here/access/github-access.md).
* **Indoor Lab:** the Indoor Lab has no RTKLib caster. Nothing indoors needs RTK: the Bebops are the only indoor quadcopters.

## Knowing the Fix Is Good

--8<-- "good-fix-quadcopter.md"
