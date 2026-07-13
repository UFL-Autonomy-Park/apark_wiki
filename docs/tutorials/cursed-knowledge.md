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
