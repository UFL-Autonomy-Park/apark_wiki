---
title: Chrony Time Sync
author: Max Gardenswartz
updated: 2026-11-06
status: active
applies_to: [apark]
assisted_by: Claude
glance: >-
  Every computer that runs our ROS 2 nodes syncs its clock with chrony to the discovery server, which serves time to the Autonomy Park network. How to set up the server and the clients.
---

Every computer that runs ROS 2 nodes for the lab runs **chrony**: the Homebrew Jetsons, the ground station computers, and the discovery server. The discovery server (`192.168.1.201` on the Autonomy Park network) is the time server. It syncs to the internet and serves time to the network. Everything else syncs to it.

This page is adapted from [TIME_SYNC.md](https://github.com/UFL-Autonomy-Park/homebrew_docker/blob/main/docs/TIME_SYNC.md) in `homebrew_docker`.

## Why

* **Message ages are computed across machines.** MAVROS stamps PX4 data with the Jetson's clock. A node on a ground computer compares that stamp with its own clock, so any offset between the two clocks goes straight into the computed age.
* **Comparing times to the millisecond.** To measure the timestamps an offboard program receives, anywhere but on the companion computer, you need chrony. Without it, the times on different computers differ by milliseconds over ROS. That can hide problems such as stale odometry, and it makes experiments harder to replicate.
* **One shared reference.** When every machine syncs to the same server, their clocks agree with each other even if the internet is slow or down.
* **No clock jumps after boot.** chrony steps the clock only in its first updates after starting (`makestep 1 3` in Ubuntu's default config), and slews it gradually afterwards. A jump while MAVROS runs makes it reset its time sync. After a battery pull, a Jetson boots with its clock at 1970 (homebrew05, 2026-10-14: chrony stepped it forward 56.8 years, 22.6 s after boot), so the `homebrew_docker` container's entrypoint waits until the clock agrees with the time server before starting ROS.
* Ubuntu's server documentation recommends chrony for serving NTP. `systemd-timesyncd`, the default client, implements SNTP only and cannot serve time.

Containers need nothing. A container cannot have its own wall clock, so the `homebrew_docker` container uses the Jetson's clock.

!!! note "chrony and systemd-timesyncd Conflict"
    On Ubuntu, installing one removes the other. All the configuration below is new files in `/etc/chrony/conf.d/`. Ubuntu's `chrony.conf` includes that directory, and the packaged `chrony.conf` is never edited.

## The Discovery Server

Run these on the discovery server computer.

1. Check the Ubuntu version and whether the firewall is active:

    ```bash
    head -2 /etc/os-release
    sudo ufw status
    ```

2. Install chrony:

    ```bash
    sudo apt-get update && sudo apt-get install -y chrony
    ```

3. Check that Ubuntu's `chrony.conf` includes the `conf.d` directory:

    ```bash
    grep -n confdir /etc/chrony/chrony.conf
    ```

    It must print `confdir /etc/chrony/conf.d`. If it prints nothing, stop: the files below would be ignored.

4. Serve time to the network, and keep serving it if the internet is lost:

    ```bash
    printf 'allow 192.168.1.0/24\nlocal stratum 10\n' | sudo tee /etc/chrony/conf.d/lan-server.conf
    ```

5. Restart chrony:

    ```bash
    sudo systemctl restart chrony
    ```

    * `allow 192.168.1.0/24` serves time to the network.
    * `local stratum 10` keeps the server answering when the internet is lost. Internet sources are stratum 1 to 3, and chrony's documentation says the local stratum should be larger than the largest stratum expected in the network.

6. Only if `ufw status` said `active`, allow the network to reach the time port:

    ```bash
    sudo ufw allow from 192.168.1.0/24 to any port 123 proto udp
    ```

7. About a minute after the restart, check that it works:

    ```bash
    chronyc sources
    chronyc tracking
    sudo ss -ulpn | grep ':123 '
    ```

    * `chronyc sources`: one line starts with `^*`, the selected internet source.
    * `chronyc tracking`: `Stratum 2` (or 3), a `Reference ID` naming an internet server, and `Leap status : Normal`. `Reference ID 7F7F0101` with `Stratum 10` means the server is on its own clock. That is normal for a few seconds after a restart, and it is what the server does when the internet is down.
    * `ss`: `chronyd` is listening on UDP port 123.

## The Homebrew Jetsons

This is part of the first-time setup in the `homebrew_docker` README (step 1.8). The commands are the same as for a ground computer, below.

## Ground Computers

Do this on any other computer that runs ROS 2 nodes.

1. Install chrony:

    ```bash
    sudo apt-get install -y chrony
    ```

2. Point it at the discovery server:

    ```bash
    printf 'server 192.168.1.201 iburst prefer\n' | sudo tee /etc/chrony/conf.d/lab-time-server.conf
    ```

3. Restart chrony and check the sources after 30 seconds:

    ```bash
    sudo systemctl restart chrony
    sleep 30
    chronyc sources
    ```

    * `iburst` sends a burst of requests at startup, so the first sync takes seconds, not minutes.
    * `prefer` uses the lab server over the internet pools from Ubuntu's default configuration. The pools stay as a fallback if the lab server is unreachable, for example when the computer is away from the lab network.

    The `192.168.1.201` line must start with `^*`. The internet pools are listed below it with `^-` (usable, not selected) or `^?` (not reachable yet). Both are normal.

4. Check the offset:

    ```bash
    chronyc tracking | grep -E "Reference ID|Stratum|System time"
    ```

    Expect `Reference ID : C0A801C9 (192.168.1.201)` and `Stratum 3`, one more than the server. `System time` is this computer's estimated offset from the server.

Clocks a few tens of milliseconds off when chrony is installed are corrected gradually, not stepped. On 2026-10-14, homebrew05 started 24 ms behind the server and was within 0.2 ms about a minute later, with no step in the chrony log (`journalctl -u chrony`), while its container kept running.

## The Indoor Lab

The Indoor Lab does not use chrony. Nothing indoors needs it today, because the Bebops are the only indoor quadcopters. It should be used there in the future, when PX4 quadcopters with companion computers are bought for the Indoor Lab.

## Undo

Undo the server **last**. Clients that still point at it fall back to the internet pools, but their clocks no longer share one reference.

### A Jetson or Ground Computer

Go back to Ubuntu's default `systemd-timesyncd`, which removes chrony:

```bash
sudo rm -f /etc/chrony/conf.d/lab-time-server.conf
sudo apt-get install -y systemd-timesyncd
timedatectl timesync-status
```

`timesync-status` should show a `Server:` line within a minute.

### The Discovery Server

1. Remove the server configuration and list the firewall rules:

    ```bash
    sudo rm -f /etc/chrony/conf.d/lan-server.conf
    sudo ufw status numbered
    ```

2. If the list has a rule for port 123, delete it by its number:

    ```bash
    sudo ufw delete <number>
    ```

3. Go back to `systemd-timesyncd`:

    ```bash
    sudo apt-get install -y systemd-timesyncd
    timedatectl timesync-status
    ```
