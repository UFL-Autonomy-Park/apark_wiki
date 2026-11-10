---
title: Software We Use
author: "Max Gardenswartz, Brandon Fallin"
updated: 2026-11-06
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  Every piece of software the lab uses, with the version, a download link, and lab-specific install notes. Check it before you install anything.
---

Every piece of software used anywhere in this wiki is listed here, with the version the lab uses and where it matters. The Download column links to each vendor's installation guide, which this wiki does not repeat. What is specific to our lab (version pins, gotchas, extra commands, troubleshooting) is in the [Lab Notes](#lab-notes) below the table.

When you write or edit a page that uses software, check that it has a row here. Add one if it does not.

| Software | Used For | Version We Use | Download | Docs / Homepage | Used On |
|---|---|---|---|---|---|
| Ubuntu | Operating system on the lab computers. Never update it. | 22.04 (22.04.5 in the installation guide) | [Ubuntu 22.04 releases](https://releases.ubuntu.com/22.04/) | [ubuntu.com](https://ubuntu.com/) | [Lab Notes](#ubuntu) |
| ROS 2 | Robot software framework | Humble | [Install ROS 2 Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) | [ROS 2 Humble docs](https://docs.ros.org/en/humble/) | [Lab Notes](#ros-2-humble), [Astro](../robots/quadcopters/freefly/astro/overview.md), [Homebrew Autonomy](../robots/quadcopters/homebrew/autonomy.md) |
| Gazebo | Simulation | Harmonic, latest minor | [Install Gazebo Harmonic](https://gazebosim.org/docs/harmonic/install_ubuntu/) | [Gazebo docs](https://gazebosim.org/docs/harmonic/) | [Lab Notes](#gazebo), [Ubuntu in VMware](ubuntu-in-vmware.md), [Ubuntu in VirtualBox](ubuntu-in-virtualbox.md) |
| PX4 | Flight controller firmware | Homebrew: 1.16.2. Astro: 1.15 base inside the Freefly bundle | [PX4 releases](https://github.com/PX4/PX4-Autopilot/releases) | [PX4 v1.16 docs](https://docs.px4.io/v1.16/) | [PX4 Configuration](../robots/quadcopters/homebrew/px4-configuration.md), [Upgrading PX4 Firmware](../robots/quadcopters/homebrew/maintain/upgrading-px4-firmware.md), [Astro](../robots/quadcopters/freefly/astro/overview.md), [Lab Notes](#px4-simulation-sitl) |
| QGroundControl (QGC) | Configuring and calibrating PX4 vehicles | Guide written for 5.1.5. On Ubuntu 22.04 use 5.0.8 or build from source | [QGC releases](https://github.com/mavlink/qgroundcontrol/releases) | [QGC docs](https://docs.qgroundcontrol.com/Stable_V5.1/en/qgc-user-guide/) | [PX4 Configuration](../robots/quadcopters/homebrew/px4-configuration.md), [Upgrading PX4 Firmware](../robots/quadcopters/homebrew/maintain/upgrading-px4-firmware.md), [Lab Notes](#qgroundcontrol-qgc) |
| MAVROS | Connects PX4 (MAVLink) to ROS 2 | 2.16.0 (tested) | [MAVROS releases](https://github.com/mavlink/mavros/releases) | No docs: either look at [MAVLink Docs](https://mavlink.io/en/) or the source code directly at [MAVROS GitHub](https://github.com/mavlink/mavros) | [Lab Notes](#mavros), [Astro](../robots/quadcopters/freefly/astro/overview.md), [RTK Setup](../hardware/rtk-setup.md) |
| Micro XRCE-DDS Agent | Planned replacement for MAVROS after PX4 1.19.0 is released; only needed because MAVROS does not support torque-level offboard commands | Not used yet | [Agent releases](https://github.com/eProsima/Micro-XRCE-DDS-Agent/releases) | [Micro XRCE-DDS docs](https://micro-xrce-dds.docs.eprosima.com/) | [Lab Notes](#planned-change-mavros-to-uxrce-dds), [Astro](../robots/quadcopters/freefly/astro/overview.md) |
| NVIDIA JetPack | Operating system and SDK on the Jetsons | 6.0 rev 2 | [JetPack](https://developer.nvidia.com/embedded/jetpack) | [JetPack](https://developer.nvidia.com/embedded/jetpack) | [Jetson Orin Nano Firmware Flashing Guide](../hardware/jetsons.md#flash-a-new-jetson-orin-nano), [Jetsons](../hardware/jetsons.md) |
| NVIDIA SDK Manager | Flashing the Jetsons | Latest | [SDK Manager](https://developer.nvidia.com/sdk-manager) | [SDK Manager docs](https://docs.nvidia.com/sdk-manager/) | [Jetson Orin Nano Firmware Flashing Guide](../hardware/jetsons.md#flash-a-new-jetson-orin-nano) |
| ZED SDK and ROS 2 wrapper | ZED 2 camera drivers | Latest | [ZED SDK releases](https://www.stereolabs.com/developers/release), [ROS 2 wrapper](https://github.com/stereolabs/zed-ros2-wrapper) | [Stereolabs docs](https://docs.stereolabs.com/) | [Homebrew Autonomy](../robots/quadcopters/homebrew/autonomy.md) |
| Docker | Running robot code on the Jetsons | Latest | [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) | [docker.com](https://www.docker.com/) | [Homebrew Autonomy](../robots/quadcopters/homebrew/autonomy.md), [Unitree B1](../robots/ground-robots/unitree/b1.md), [RTK Setup](../hardware/rtk-setup.md) |
| ZeroTier | VPN to the Autonomy Park network | Latest | [ZeroTier downloads](https://www.zerotier.com/download/) | [ZeroTier docs](https://docs.zerotier.com/) | [ZeroTier VPN Install](../networking/zerotier-vpn-install.md), [File Backup Server](../networking/file-backup-server.md) |
| Auterion CLI | Installing apps on the Astros | Latest | [Auterion CLI](https://docs.auterion.com/app-development/resources/auterion-cli) | [Auterion docs](https://docs.auterion.com/) | [Astro](../robots/quadcopters/freefly/astro/overview.md) |
| Mission Planner | Updating the Here4 GNSS firmware | Latest | [Mission Planner installer (.msi)](https://firmware.ardupilot.org/Tools/MissionPlanner/MissionPlanner-latest.msi) | [Mission Planner docs](https://ardupilot.org/planner/) | [Updating Here4 GNSS Firmware](../robots/quadcopters/homebrew/maintain/updating-here4-gnss-firmware.md) |
| OptiTrack Motive | Motion capture in the Indoor Lab | 2.0.2. Needs the USB license key (see Mocap Calibration). May not run on newer Windows | [Motive 2.0.2 installer (no login)](https://drive.google.com/file/d/1-iwubh2fYvJMuSaYW6uyuK_54jqeBLSN/view?usp=drive_link), [OptiTrack downloads](https://optitrack.com/support/downloads/) | [Motive](https://optitrack.com/software/motive/) | [Mocap Calibration](../hardware/mocap-calibration.md) |
| VMware, VirtualBox | Running Ubuntu in a virtual machine | Latest | [VMware Workstation and Fusion](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion), [VirtualBox downloads](https://www.virtualbox.org/wiki/Downloads) | [vmware.com](https://www.vmware.com/), [virtualbox.org](https://www.virtualbox.org/) | [Ubuntu in VMware](ubuntu-in-vmware.md), [Ubuntu in VirtualBox](ubuntu-in-virtualbox.md), [Lab Notes](#ubuntu) |
| RTKLib | Serves RTK corrections to the quadcopters (the caster) | 2.4.3 (very stable; no update since 2020) | [RTKLib releases](https://github.com/tomojitakasu/RTKLIB/releases) | [RTKLib on GitHub](https://github.com/tomojitakasu/RTKLIB) | [RTK Setup](../hardware/rtk-setup.md), [Setting Up RTK on the Astros](../robots/quadcopters/freefly/astro/rtk-setup.md) |
| Emlid Flow | Mobile app that configures the Emlid ground station and rovers | Latest | [App Store](https://apps.apple.com/us/app/emlid-flow/id1463967138), [Google Play](https://play.google.com/store/apps/details?id=com.emlid.reachview3) | [Emlid Flow](https://emlid.com/emlid-flow/), [Emlid docs](https://docs.emlid.com/) | [RTK Setup](../hardware/rtk-setup.md) |
| uv | Python environment for this wiki | Latest, locked in `uv.lock` | [Install uv](https://docs.astral.sh/uv/getting-started/installation/) | [uv docs](https://docs.astral.sh/uv/) | [Edit the Wiki](../start-here/edit-the-wiki.md) |
| Git, Git LFS | Version control for this wiki | Latest | [Git downloads](https://git-scm.com/downloads), [Git LFS](https://git-lfs.com/) | [git-scm.com](https://git-scm.com/), [git-lfs.com](https://git-lfs.com/) | [Edit the Wiki](../start-here/edit-the-wiki.md) |

## Lab Notes

Only what the vendor guides lack. The steps for the simulation setup come in this order: ROS 2, QGroundControl, Gazebo, PX4, then MAVROS.

### Ubuntu

All the park's equipment requires **Ubuntu 22.04.5 (Jammy Jellyfish)** for complete functionality of the park's resources (ROS 2 Humble needs it). Keep the version you installed and **never update Ubuntu**.

For a complete tutorial on running Linux in a virtual machine on Windows for a general ROS 2 project, see [Ubuntu in VMware](ubuntu-in-vmware.md) (written steps) or [Ubuntu in VirtualBox](ubuntu-in-virtualbox.md) (video). Apple Silicon Macs are not covered by either: they need an ARM-based Ubuntu, and some things, such as GPU acceleration for Gazebo, will not work.

!!! note "Virtual Machine Disk Space"
    For general tutorials and work, 20 GB of allocated disk space works well. For larger projects with PX4 and Gazebo, 20 GB is not sufficient. Allocate a minimum of 40 GB, and 50 to 60 GB for good overall performance.

### ROS 2 Humble

The installation steps are exactly the same as in the vendor guide linked above. A video walkthrough:

<iframe width="560" height="315" src="https://www.youtube.com/embed/tvToTLZQkZI" title="ROS 2 Humble install walkthrough" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

To test the installation, run the talker example from the vendor guide in one terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

Run the listener in another terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

The talker should say it is publishing messages and the listener should say it heard them. This verifies both the C++ and Python APIs.

### QGroundControl (QGC)

--8<-- "qgc-ubuntu-warning.md"

In a new terminal, add yourself to the dialout group, remove ModemManager, and install the packages QGC needs:

```bash
sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
sudo apt install libfuse2 -y
sudo apt install libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor-dev -y
```

Download `QGroundControl.AppImage` from the download link, move it to a folder of your choice (for example `~/Downloads`), make it executable, and run it:

```bash
chmod +x ~/Downloads/QGroundControl.AppImage
~/Downloads/QGroundControl.AppImage
```

### Gazebo

PX4 SITL uses Gazebo Harmonic. Install it following the vendor guide linked above.

### Planned Change: MAVROS to uXRCE-DDS

The lab plans to move offboard control of the quadcopters from MAVROS to the Micro XRCE-DDS Agent (uXRCE-DDS), PX4's native connection to ROS 2. Nothing changes yet: MAVROS is still the path described on this page as of 2026-10-21.

Why: MAVROS does not support torque-level offboard commands, and uXRCE-DDS does. In the lab's current setup, though, using uXRCE-DDS means giving up RTK. As of PX4 1.17.0 (and so 1.16.2), the Micro XRCE-DDS Agent exposes no topic for serving RTK corrections. With MAVROS, an NTRIP client on a companion computer publishes them to `<mavros_namespace>/mavros/gps_rtk/send_rtcm`.

A PX4 change Max test flew for the PX4 devs addresses that. [PX4 pull request #29368](https://github.com/PX4/PX4-Autopilot/pull/29368) will let ROS 2 applications send RTK (RTCM) corrections to PX4 over uXRCE-DDS. As of 2026-11-10 it is merged, butis not part of any stable PX4 release (the release that will include it: *Unknown*{ .unknown }). To experiment with torque-level control together with RTK, you must build mainline PX4 and port every parameter to the current [PX4 parameter reference](https://docs.px4.io/main/en/advanced_config/parameter_reference).

### MAVROS

In a new terminal, install MAVROS and its dependencies:

```bash
sudo apt install ros-humble-mavros ros-humble-mavros-extras
sudo apt install ros-humble-geographic-msgs
sudo apt install geographiclib-tools
sudo apt install libgeographic-dev
sudo apt install geographiclib-doc
```

Create the GeographicLib directories if they do not exist:

```bash
sudo mkdir -p /usr/share/GeographicLib/geoids
sudo mkdir -p /usr/share/GeographicLib/gravity
sudo mkdir -p /usr/share/GeographicLib/magnetic
```

Install the egm96-5 dataset manually:

```bashd
sudo geographiclib-get-geoids egm96-5
```

With PX4 running in a separate terminal (see above), launch MAVROS. It connects to PX4 over MAVLink. Autonomy Park SITL does this for you.

```bash
source /opt/ros/humble/setup.bash
ros2 launch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
```