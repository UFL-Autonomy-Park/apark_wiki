---
title: "Case Study: Lidar and CAN Sensor Burnout"
author: Max Gardenswartz
updated: 2026-11-10
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  Lidars wired any way except the included connector on I2C 2 slowly burn out other sensors on the CAN bus, and a lidar that is already failing can damage the next drone it is plugged into. This is how the problem was found.
---

--8<-- "lidar-wiring-danger.md"

## The Symptom

During bench tests on 2026-05-01 on Homebrew 08, the lidar reading (helps with height estimation) flickered rapidly between a sensible value and 0 on MAVLink Inspector (a page on QGC). The lidar was plugged into the flight controller (FC) via the CAN Extender using a custom-soldered connector. Whenever the battery was disconnected (thus power was given by USB only), flickering stopped. Readings reacted normally to changes in distance to ground.

Upgrading software and different drones with the same parameters exhibited the same behavior. 

The two photos below show the same area of a Homebrew. The circled parts are the lidar wiring.

![A Homebrew's flight controller area with a circled two-wire red and black lead ending in a small white connector, the custom-soldered lidar connector.](../../../../images/homebrew/lidar-wired-incorrectly.jpg){ width="60%" }

*Incorrect: the lidar is wired with a custom-soldered connector. Never power it on.*

![A Homebrew's flight controller area with a circled multi-colored lidar cable plugged into a small black adapter board labeled CON2.](../../../../images/homebrew/lidar-wired-correctly.jpg){ width="60%" }

*Correct: the lidar's included cable on its adapter board.*

## The Homebrew 05 Crash

On 2026-01-31, Homebrew 05 crashed during a manual flight in Position Mode. It drifted massively without any command and moved in a random "toilet bowling" pattern. This was all later traced to the custom connector on the lidar, used instead of the included one.

<figure markdown="span">
  <video src="../../../../../videos/homebrew-05-crash-2026-01-31.mp4" autoplay loop muted playsinline controls width="100%"></video>
  <figcaption>Homebrew 05 crash, 2026-01-31: manual flight in Position Mode with uncommanded drift and toilet bowling.</figcaption>
</figure>

## What Was Found Later

* The flicker happens because two distance sensors are on the same CAN bus. The optical flow sensor has a distance sensor too. When the battery was connected, optical flow could then publish over the CAN, which clashed with the readers of the lidar due to the lidar's incorrect wiring.
* The optical flow sensor and the distance sensor are very close to each other on the drone, making it difficult to test which sensor PX4 was using. PX4 auto-selects a new distance sensor if data is stale or invalid for more than 1.0 second.
* Cutting and re-terminating the lidar cable (as half the Homebrews have!), or otherwise using anything but the included lidar connector, slowly burns out the lidar and other CAN sensors over time like the optical flow sensor.
* The fix is to connect the lidar with **its included cable** and using **I2C 2**, not the CAN extender.

According to the PX4 logs, the lidar and optical flow on Homebrew 03 failed **before** its crash on 2026-10-09. As of its successful offboard flight on 2026-10-07, both sensors were working. While investigating, a lidar from a bad setup was found to damage other quadcopters whose lidar was failing or had already failed when it was connected to them. Whether the damaged sensors are recoverable is unknown and has not been investigated. The lidar units cost $400 apiece, so this is a good long-term task. However, since Max got RTK working on the Homebrews, optical flow and lidar are actually unnecessary and actually (very) slightly make PX4's setpoint tracking and ability to hold in Position Mode slightly worse!

## What to Do

* Use I2C 2 and the lidar's included cable. Do not cut the cable.
* Do not move a lidar from a drone with bad wiring to another drone. It can burn out other sensors on the CAN like the optical flow sensor. 
* The status of whether each Homebrew's lidar is wired correctly or not is given in [Known Issues](../known-issues.md#status-of-each-homebrew).

## Related

* [Case Study: The Homebrew 03 Crash From a Saturated MAVROS Link](mavros-link-saturation.md)
