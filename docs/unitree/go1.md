---
title: Unitree Go1
---

# Unitree Go1

## IP Reservations

| **Device Name** |   **Username**    | **IP Address** | **Password** |
| :-------------: | :---------------: | :------------: | :----------: |
|     doggo1      |   doggo-jetson    | 192.168.1.153  |     1234     |
|     doggo2      |   doggo-jetson2   | 192.168.1.154  |     1234     |
|     doggo3      |   doggo-jetson3   | 192.168.1.165  |     1234     |
|    BigDoggo     | big-doggo1-jetson |  192.168.1.67  |    12345     |

## Dog Startup Instructions

SSH into the dog's Jetson - the username and IP address is labeled on the side of the dog.

```
$ ssh doggo_username@192.168.1.dog_ip_addr
# enter password
$ 1234
# run screen to ensure the terminal isn't killed on disconnect
$ screen
# click space a couple times till all the text goes away
# run the docker container
./openDockerDogsHumble.sh
# go into the localFiles folder
$ cd /home
# run the ros2 startup script
$ ./runUnitreeMinimalStartup.sh
```

When finished using the robot, click 'Ctrl+C' to kill ROS.

```
# exit the docker container
$ exit
```

Kill the screen window - click 'Ctrl-A+K' then 'Y' to confirm killing the session.

```
# exit the ssh session
$ exit
```

## Manual

[Go1 Manual](../../unitree/go1-manual.pdf)

## Harness/Frame

[Harness Manual](../../unitree/harness-manual.pdf)
