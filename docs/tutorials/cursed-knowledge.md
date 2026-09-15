---
title: Cursed Knowledge
---

Ever had to troubleshoot an error in software, or tinker with hardware for hours just to find out there was a really simple fix? If so, document it here to save someone else some time. 

## NVIDIA Jetson `apt` Sources
Run this in terminal if your sources are messed up:

```bash
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/cache/app-info
sudo apt clean
sudo apt update
```

## Homebrews
The Optical Flow sensor has a built-in distance sensor.
The LiDaR is usually the primary distance sensor.
When I say "distance" sensor, I mean the sensor used for the purposes of local altitude estimation (not AMSL or ellipsoidal of course).
PX4 will fallback to which ever one it detects first. Usually, it every time was plugged in correctly, that will mean the LiDAR. However, if your LiDAR is broken or unplugged, you will never know because the fallback check happens once on boot and will never change without a reboot.