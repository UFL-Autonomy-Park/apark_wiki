---
title: Lab Rules
author: Max Gardenswartz
updated: 2026-11-10
status: active
status_note: This list is not complete. Rules are added as they are decided.
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  The rules everyone follows in the lab, in one short list. Read it before you fly, charge a battery, or use anything.
---

## General Rules

* **All hardware belongs to Dr. Kamalapurkar.** We do not lend hardware to anyone outside the SCC roster.
* **No removing robots/equipment from the Autonomy Park.** SCC Lab Members are exempt.
* **Do not leave the Emlid RTK units outside.** It's not waterproof and it's expensive to replace. Bring inside when done.
* **Read the documentation for a robot before you use it.** Every robot has pages in the Robots tab. Read all of them first.
* **Safety glasses are required outdoors.**
* **No operating robots in weather.** Rain and high wind ruin equipment. Bring it inside.
* **Minimize spectators.** Our labs are for research and must be shared. Lots of unnecessary workers can become a safety issue.
* **Every robot must have an RC with a kill switch.** For quadcopters, a disarm switch **will not cut it**. For ground robots, this usually means a dead-man switch.
* **Keep things nice.** Put all robots away when done, close the blinds, and turn off all lights.
* **Report all crashes and injuries to Dr. Kamalapurkar.** See [Report an Incident](report-an-incident.md).

## Flying

* **No flying vehicles outside the net.** It's illegal. No exceptions.
* **Never enter the net while a quadcopter is armed or flying.** Disarm it first.
* **No benchwork on drones with batteries and propellers on at the same time.** We've had people get seriously injured by unexpected spinning.
* **Watch flying vehicles at all times.** Don't get distracted with your code or a visualizer.

## LiPo Batteries

* **Never leave a charging battery unattended.** Charge only with the approved charger, on a non-flammable surface.
* **Never charge or fly a battery that is hot, damaged, or swollen.**
* **Never charge above 4.2 V per cell, and never discharge below 3.0 V per cell.** Any cell outside those limits is permanently damaged. Chargers generally prevent over-charging. Only you can prevent over-discharging.
* **Never puncture a battery, carry it by its leads, or throw it in the trash.**
* **Put a dropped, damaged, swollen, old, or wrongly charged battery in the ammo can, and tell a lab manager right away.** Tape any severed leads first. The Autonomy Park's ammo can is in the storage shed by the Venom chargers. The Indoor Lab's is on a bottom shelf in the Indoor Lab.
* **Don't fight LiPo battery fires. Get to safety and call 911.** Never use an extinguisher, water, or sand.

## Hardware-Specific

* **Those using Dr. Kamalapurkar's drones (Astros and Homebrews) for off-board control must simulate in [Autonomy Park SITL](https://github.com/UFL-Autonomy-Park/autonomy_park_sitl) first** for safety reasons.
* **No custom firmware/autopilots.** Especially for quadcopters, this is a safety risk.
* **Control barrier functions (CBFs) are required for multi-agent experiments.** CBFs for offboard control do not exist yet, and more RFD 900x radios must be bought, so multi-agent experiments are not possible right now.
* **Every Homebrew needs an RFD 900x radio to fly** for safety reasons. Otherwise, your off-board program is the sole failure point for getting a drone to land safely (very dangerous!).

## Soldering

* **No leaded solder.** Leaded waste requires a pick-up. You also cannot mix lead and lead-free solder.
* **Wash your hands after soldering.** Treat it as though it were leaded.
* **Replace the iron in the holder and turn it off when done.** It's a fire risk.

[Safety](safety.md){ .md-button }
[Report an Incident](report-an-incident.md){ .md-button }
[Contacts](contacts.md){ .md-button }
