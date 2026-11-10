---
title: NTRIP Caster for RTK on Quadcopters
author: Max Gardenswartz
updated: 2026-11-10
applies_to: [apark]
assisted_by: Claude
glance: >-
  How the Autonomy Park's local NTRIP caster is built from the Emlid RS3 and RTKLIB's str2str, so the quadcopters get RTK corrections over the network. Reference only: the caster is already running.
---

!!! note "Reference Only"
    This page is for reference. The Autonomy Park's `discovery` computer (see [IP Reservations](../software/ip-reservations.md)) is already set up as the caster described below. You do not need to follow these steps to use RTK. To use RTK on a robot, see [RTK Setup](../hardware/rtk-setup.md).

!!! warning "A Username and Password Are Required"
    The caster will not start without a username and password. Every command below that starts it has them in the stream path as `<username>:<password>`. Replace both with the real values, which are not on the wiki: see [Contacts](../start-here/contacts.md). Every client needs the same pair.

This is the setup that is running on the `discovery` computer (Ubuntu 22.04, RTKLIB `str2str`), written up with the fixes found along the way, a section on the required username and password, and a section for undoing everything. It was last written up on 2026-10-16.

## The Values Used

Replace these if the network changes.

| Name | Value | Meaning |
|---|---|---|
| RS3 address | `192.168.1.13` | The Emlid RS3 on the Wi-Fi network |
| RS3 TCP port | `9000` | Port the RS3 listens on once its output is set to TCP, role Server |
| Caster computer | `discovery` (`192.168.1.201`) | The Ubuntu 22.04 computer running `str2str` |
| Caster port | `2101` | Port the robots connect to |
| Mountpoint | `BASE` | The name of the stream in the URL. Any name works if every client uses the same one |
| Service name | `ntrip-caster` | The systemd unit |
| Service user | `rtk` | A system user with no login that owns the service and the logs |
| Log directory | `/var/log/rtcm` | Raw RTCM3 recordings |

## How It Fits Together

```text
Emlid RS3 (192.168.1.13)            discovery (192.168.1.201)                 robots
  TCP server :9000  <-- connects --  str2str  -->  caster :2101 / BASE  -->  Freefly NTRIP client
  (raw RTCM3)                           |                                --> lordmicrostain ROS 2 client
                                        +--> /var/log/rtcm/*.rtcm3 (hourly files, size-capped)
```

The RS3 has one connection (to `discovery`) instead of one per robot. `str2str` passes the RTCM3 bytes through unchanged and fans them out to every client.

## What Has Been Verified

| Item | How it was checked | Result |
|---|---|---|
| `ntripc://` caster output exists in the Ubuntu 22.04 binary | `str2str -h \| grep ntripc` on `discovery` | Works. The Ubuntu man page does not list it, but the binary does |
| RS3 TCP stream reaches the computer | `str2str` status line on `discovery` | RS3 connected, about 4.1 kbps |
| Caster serves data locally and from another computer | `curl --http0.9` on `discovery` and on `superman` | `ICY 200 OK` then RTCM3 frames (message types 1124 and 1006 seen) |
| Service starts and records logs | `systemctl status`, `ls /var/log/rtcm` on `discovery` | Active, enabled at boot, log files growing |
| 8 simultaneous clients | Test run against upstream RTKLIB b34 with a fake RS3 | All 8 received data |
| Username and password | Same test setup, `curl -u` | See the username and password section |
| Log pruning script, user creation and removal | Same test setup | Worked |
| Hourly cron entry | Not tested | The test setup had no cron installed |
| Freefly and lordmicrostain clients | Not tested | Still the real acceptance test |
| Reboot and RS3 power-cycle recovery | Not tested | |
| Hourly log rotation | Expected from the source, not yet confirmed | Look for a file like `20261016_0000.rtcm3` |

## Make the RS3 a Raw TCP Server

1. In Emlid Flow, open the base's correction output and choose **TCP**.
2. Set the role to **Server**, address `localhost`, port `9000`. These are the settings Emlid staff gave in a forum answer ([forum thread](https://community.emlid.com/t/base-rover-settings-over-tcp-wifi/12147)). The official RS3 docs page for this screen could not be loaded, so go by what Flow shows.
3. Choosing TCP replaces the NTRIP server output, so there is nothing separate to switch off.
4. Give the RS3 a fixed address (for example a DHCP reservation).
5. Emlid's docs say Reach receivers can broadcast on two output channels at once (Base output 1 and Base output 2), which could let the ground robots keep LoRa while the computer takes TCP. The page does not list which pairs work ([Dual base output](https://docs.emlid.com/reachrs3/base-setup/dual-base-output/)). Two TCP outputs need different ports.

Check that the RS3 is sending, from the computer. The first command checks that the port accepts a connection. The second prints the first bytes of the stream, and RTCM3 frames start with byte `d3`.

```bash
RS3_IP=192.168.1.13
nc -zv -w 3 $RS3_IP 9000
nc -w 3 $RS3_IP 9000 | head -c 64 | od -An -tx1
```

`connection refused` means the RS3's TCP output is not enabled yet. A timeout means the computer cannot reach the RS3.

## Install RTKLIB

```bash
sudo apt update && sudo apt install rtklib
apt policy rtklib
str2str -h 2>&1 | grep ntripc
```

Expect version `2.4.3.b34+dfsg-1` from `apt policy`, and an `ntripc` line from the `grep`. The package contains `/usr/bin/str2str` ([file list](https://packages.ubuntu.com/jammy/amd64/rtklib/filelist)). If the `grep` prints nothing, build from source:

```bash
git clone --depth 1 --branch rtklib_2.4.3 https://github.com/tomojitakasu/RTKLIB.git
cd RTKLIB/app/consapp/str2str/gcc && make
sudo install -m 755 str2str /usr/local/bin/str2str
```

Then use `/usr/local/bin/str2str` in the service file below.

## Run the Caster by Hand

```bash
str2str -in tcpcli://192.168.1.13:9000 -out ntripc://<username>:<password>@:2101/BASE
```

* `-in tcpcli://...`: `str2str` connects to the RS3 as a TCP client.
* `-out ntripc://<username>:<password>@:2101/BASE`: it listens on port 2101 and serves the mountpoint `BASE`. The username and password are required.
* No `#rtcm3` on any stream: bytes pass through untouched. Format conversion only happens when both the input and an output carry `#format`, and its default message list is `1004,1019`, which would replace the RS3's messages.
* Status line, every 5 seconds: the characters are input, then each output. `E` is an error, `-` is closed, `W` is waiting, and `C` is connected. `[CWC--]` means the RS3 is connected, the caster is waiting for clients, and the log file is open. `[CCC--]` appears when a client is connected.
* The timestamps on that line are GPS time, 18 seconds ahead of UTC.
* If the RS3 drops, `str2str` retries every 10 s by default.

Test it as a client would:

```bash
curl -s --http0.9 -m 3 -i http://localhost:2101/
curl -s --http0.9 -m 3 -u <username>:<password> -H "Ntrip-Version: Ntrip/2.0" http://localhost:2101/BASE | head -c 40 | od -c
```

The first command fetches the sourcetable and the second fetches the stream. Expect `SOURCETABLE 200 OK` with a bare `STR;BASE;` entry, then `ICY 200 OK` followed by byte `0xD3` (octal `323`). The curl option `--http0.9` is required because curl 8.5 refuses the caster's `ICY 200 OK` reply otherwise. The second command exits with code 28 (timeout) because the stream never ends.

Things learned in testing:

* A client request without a `User-Agent` header gets an empty reply (the caster drops it).
* The mountpoint is whatever follows the first `/` in the request path and must equal `BASE` exactly. A request for any other mountpoint returns the sourcetable instead of data.
* **Do not run this command by hand while the service is running.** Both want port 2101, and the second one fails with `stream server start error`. Stop the service first with `sudo systemctl stop ntrip-caster`.

## Run It as a Service with Logging

```bash
sudo useradd -r -s /usr/sbin/nologin rtk
sudo mkdir -p /var/log/rtcm && sudo chown rtk /var/log/rtcm
```

Put this in `/etc/systemd/system/ntrip-caster.service`:

```ini
[Unit]
Description=RTKLIB NTRIP caster for Emlid RS3
After=network-online.target
Wants=network-online.target

[Service]
User=rtk
ExecStart=/usr/bin/str2str -in tcpcli://192.168.1.13:9000 \
  -out ntripc://<username>:<password>@:2101/BASE \
  -out file:///var/log/rtcm/%%Y%%m%%d_%%h%%M.rtcm3::S=1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then start it and follow its log:

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now ntrip-caster
journalctl -u ntrip-caster -f
```

* `%%` in a unit file becomes a literal `%`. Log file names like `20261015_2343.rtcm3` show this works.
* Log file names use UTC (GPS time), not local time. `S=1` swaps files every hour.
* If the service fails with `stream server start error`, one stream could not open. Reproduced causes are a busy port 2101 (`sudo ss -ltnp | grep 2101`) and a log directory the `rtk` user cannot write (`sudo -u rtk touch /var/log/rtcm/write_test`).

## Cap the Log Size

This script deletes the oldest closed RTCM logs until the directory is under a size limit. It never deletes the newest file, because that one is still being written. The size limit is in MB and defaults to 20480 (20 GB, an arbitrary choice; change it).

```bash
sudo tee /usr/local/bin/rtcm-prune.sh >/dev/null <<'EOF'
#!/bin/bash
DIR="${1:-/var/log/rtcm}"
MAX_MB="${2:-20480}"
MAX_BYTES=$((MAX_MB * 1024 * 1024))
while :; do
  total=$(find "$DIR" -maxdepth 1 -type f -name '*.rtcm3' -printf '%s\n' | awk '{s+=$1} END{print s+0}')
  [ "$total" -le "$MAX_BYTES" ] && break
  count=$(find "$DIR" -maxdepth 1 -type f -name '*.rtcm3' | wc -l)
  [ "$count" -le 1 ] && break
  oldest=$(find "$DIR" -maxdepth 1 -type f -name '*.rtcm3' -printf '%T@ %p\n' | sort -n | head -n1 | cut -d' ' -f2-)
  rm -f -- "$oldest"
done
EOF
sudo chmod 755 /usr/local/bin/rtcm-prune.sh
```

Test it on throwaway files before trusting it with real logs. Expect `f3`, `f4` and `f5` to be left.

```bash
mkdir /tmp/prunetest && for i in 1 2 3 4 5; do head -c 1048576 /dev/zero > /tmp/prunetest/f$i.rtcm3; touch -d "2026-10-1$i 00:00" /tmp/prunetest/f$i.rtcm3; done
/usr/local/bin/rtcm-prune.sh /tmp/prunetest 3 && ls /tmp/prunetest
rm -r /tmp/prunetest
```

Run it hourly. The first command checks that both succeed (the hourly folder exists and cron is active).

```bash
ls -d /etc/cron.hourly && systemctl is-active cron
printf '#!/bin/sh\n/usr/local/bin/rtcm-prune.sh /var/log/rtcm 20480\n' | sudo tee /etc/cron.hourly/rtcm-prune >/dev/null
sudo chmod 755 /etc/cron.hourly/rtcm-prune
sudo /etc/cron.hourly/rtcm-prune && echo "ran OK"
```

## Configure the Clients

Both clients take host `192.168.1.201`, port `2101`, and mountpoint `BASE`.

* **Freefly:** fill in the username and password fields.
* **lordmicrostain ROS 2 client:** set `authenticate` to `true` and fill in `username` and `password`. The README says both must be supplied in that case ([README](https://github.com/LORD-MicroStrain/ntrip_client)).
* **dotenv file:** use `NTRIP_MOUNTPOINT=BASE` with no leading slash.
* `ntrip_version`: the README does not list accepted values. Keep whatever your template uses for version 2. The caster does not check that header.
* If a client shows no data, check the caster's status line: the second character should change from `W` to `C` when a client connects. Common causes are a missing `User-Agent` header, a wrong mountpoint, or a client that rejects the `ICY 200 OK` reply. None of these has been observed with the real clients yet.

## The Username and Password

The caster needs one username and one password for the mountpoint, and it will not start without them. In the stream path the format is `ntripc://<username>:<password>@:2101/BASE`. This was tested against upstream RTKLIB b34 with `curl`:

| Request | Result |
|---|---|
| No credentials, correct mountpoint | `HTTP/1.0 401 Unauthorized` |
| Right username, wrong password | `HTTP/1.0 401 Unauthorized` |
| Wrong username, right password | `HTTP/1.0 401 Unauthorized` |
| Correct credentials | `ICY 200 OK` followed by RTCM3 data |

### Set or Change Them

1. Pick a username and a password. Use letters and digits only. Special characters were not tested, and the stream path is split on `@`, `:` and `/`.
2. Edit the service file and change the caster line, replacing `<username>` and `<password>` with yours:

    ```ini
    -out ntripc://<username>:<password>@:2101/BASE \
    ```

3. Apply it and test. The first `curl` should print `HTTP/1.0 401 Unauthorized`. The second should print `ICY 200 OK`.

    ```bash
    sudo systemctl daemon-reload && sudo systemctl restart ntrip-caster
    curl -s --http0.9 -m 3 -i http://localhost:2101/BASE | head -c 60
    curl -s --http0.9 -m 3 -u <username>:<password> http://localhost:2101/BASE | head -c 12 | od -c
    ```

4. Update every client at the same moment, or the ones you did not update will be refused.

### What This Does and Does Not Protect

* The username and password are visible to anyone who can run `ps` on `discovery`, and in `systemctl status`. In the test, `ps` showed the full command line including the password.
* The sourcetable (`curl http://localhost:2101/`) is still served without credentials. The caster checks the mountpoint before it checks the password.
* HTTP Basic authentication sends the credentials without encryption (they are only base64-encoded). That is fine for a lab network and not for the open Internet.
* The password stops other devices from pulling the stream. Anyone on the network can still see that the caster exists and which mountpoint it serves, because of the open sourcetable above.

## Undo Everything

Work through these in order. The service must be stopped before its user and log directory are removed.

### Remove the Caster from the Computer

```bash
sudo systemctl disable --now ntrip-caster
sudo rm /etc/systemd/system/ntrip-caster.service
sudo systemctl daemon-reload
sudo rm -f /etc/cron.hourly/rtcm-prune /usr/local/bin/rtcm-prune.sh
sudo rm -r /var/log/rtcm
sudo userdel rtk
```

`rm -r /var/log/rtcm` deletes all recorded RTCM logs, so copy any you want to keep first. `userdel rtk` removes the user and its same-named group.

Optional, only if nothing else on `discovery` uses RTKLIB. The second command is only needed if you built from source.

```bash
sudo apt remove rtklib
sudo rm -f /usr/local/bin/str2str
```

In testing, `useradd -r` created both a user and a group named `rtk` and no home directory, and `userdel rtk` removed the user and the group. The `apt remove` step was not tested.

### Check That It Is Gone

```bash
systemctl status ntrip-caster
sudo ss -ltnp | grep 2101
getent passwd rtk
ls /var/log/rtcm /usr/local/bin/rtcm-prune.sh /etc/cron.hourly/rtcm-prune
```

The first command should report that the unit could not be found. The second and third should print nothing. The last should say "No such file" for all three.

### Put the Rest Back the Way It Was

These are outside `discovery` and are not covered by the commands above:

1. **RS3:** in Emlid Flow, set the base correction output back to the setting you used before (the RS3 as its own NTRIP server and caster), and disable the TCP output.
2. **Clients:** point the Freefly and lordmicrostain clients back at the RS3's own NTRIP settings and remove `192.168.1.201` and `BASE` from their configuration.

This guide did not touch chrony, ROS discovery, or any firewall (the computer has none, so no port was opened), so there is nothing to undo there.

## Sources

* [Ubuntu 22.04 `str2str` man page](https://manpages.ubuntu.com/manpages/jammy/man1/str2str.1.html)
* [Ubuntu 22.04 `rtklib` source package](https://packages.ubuntu.com/source/jammy/rtklib)
* [`rtklib` jammy file list](https://packages.ubuntu.com/jammy/amd64/rtklib/filelist)
* [RTKLIB `stream.c` (b34)](https://raw.githubusercontent.com/tomojitakasu/RTKLIB/rtklib_2.4.3/src/stream.c)
* [RTKLIB `str2str.c` (b34)](https://raw.githubusercontent.com/tomojitakasu/RTKLIB/rtklib_2.4.3/app/consapp/str2str/str2str.c)
* [Emlid RS3: Dual base output](https://docs.emlid.com/reachrs3/base-setup/dual-base-output/)
* [Emlid forum: base/rover TCP settings](https://community.emlid.com/t/base-rover-settings-over-tcp-wifi/12147)
* [Emlid RTCM3 message table (RS2 docs)](https://docs.emlid.com/reachrs2/specifications/rtcm3-format/)
* [lordmicrostain `ntrip_client` README](https://github.com/LORD-MicroStrain/ntrip_client)
