---
title: Homebrew Drone Build
---

## Video Guides

[Boot Jetson with SSD instead of SD card](https://www.youtube.com/watch?v=q4fGac-nrTI)

[RFD900x Wiring](https://www.youtube.com/watch?v=UBxZTWxYdXM)

## Physical Measurements

| **Component Name** | **X [m]** | **Y [m]** | **Z [m]** |
| :----------------: | :-------: | :-------: | :-------: |
| Flight Controller  |  0.0587   |    0.0    |    0.0    |
|        GPS         |  0.00952  |    0.0    |   0.217   |
|       LIDAR        | -0.00635  |  0.0539   |   0.114   |
|    Optical Flow    |  0.0444   |  0.0667   |  0.0508   |

## NVIDIA Jetson

Run this in terminal if your sources are messed up:

```
sudo rm -rf /var/lib/apt/lists/*
sudo rm -rf /var/cache/app-info
sudo apt clean
sudo apt update
```

## MAVROS Dockerfile, Startup Script

`start_mavros.service` located at `\etc\systemd\system\`

```
[Unit]
Description=Start MAVROS on boot
After=network-online.target docker.service

[Service]
Type=simple
ExecStart=/path/to/your/script/start_mavros.sh
User=yourusername

[Install]
WantedBy=multi-user.target
```

`start_mavros.sh` located at `\home\yourusername`

## MAVROS Parameters

MAVROS parameters (including tuned PID gains) can be found [here](../../homebrew/homebrew.params)

## Manuals

[Battery Manual](../../homebrew/tattu-manual.pdf)

[LIDAR Manual](../../homebrew/lidar-manual.pdf)

[Here 4 GPS Manual](https://docs.cubepilot.org/user-guides/here-4/here-4-manual)
