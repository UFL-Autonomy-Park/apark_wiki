# Installation/Simulation Setup for ROS2, MAVROS, PX4, and QGroundControl

This guide will walk through how to set up the development environment to control the aerial and ground robots at the Autonomy Park.

For the park, all equipment requires **Linux Ubuntu Version 22.04.5 (Jammy Jellyfish)** to have complete functionality of park resources (needed for ROS2 Humble).
This means keeping the current version when installed and **never updating Ubuntu**.

For a complete tutorial on getting a virtual machine to run Linux locally on Windows for general ROS2 project, see this link: [https://autonomypark.org/ROS/vmware-guide.pdf](https://autonomypark.org/ROS/vmware-guide.pdf). 
**NOTE:** For the VM, you will have to allocate disk space and for general tutorials/work, 20 GB works well. However, for larger projects working with the PX4 and Gazebo, 20 GB is not sufficient. It's recommended minimum 40GB for allocated space and between 50-60GB allocated for good overall performance.

## ROS2 Humble Installation

First we will download ROS2 Humble: [https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html). 
The steps are exactly the same here as on the site for what we use.


```
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

```
sudo apt install software-properties-common
sudo add-apt-repository universe
```

```
sudo apt update && sudo apt install curl -y
```

```
sudo curl -sSL [https://raw.githubusercontent.com/ros/rosdistro/master/ros.key](https://raw.githubusercontent.com/ros/rosdistro/master/ros.key) -o /usr/share/keyrings/ros-archive-keyring.gpg
```

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] [http://packages.ros.org/ros2/ubuntu](http://packages.ros.org/ros2/ubuntu) $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

```
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-humble-ros-base
sudo apt install ros-dev-tools
```

To test if everything is downloaded properly for ROS2, do this example on the page:

In one terminal type:
```
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

In another terminal type:
```
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

With this set up, you should see: The talker saying that it’s Publishing messages and the listener saying I heard those messages.This verifies both the C++ and Python APIs are working properly. 

## QGroundControl Installation

QGroundControl Download link: [https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html).

In a new terminal:

```
sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
sudo apt install libfuse2 -y
sudo apt install libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor-dev -y
```

Now go on the site and download the QGroundControl.AppImage and move it to your file of choice (e.g., Downloads). Make it executable and run it (example assumes it's in Downloads):

```
chmod +x ~/Downloads/QGroundControl.AppImage
~/Downloads/QGroundControl.AppImage
```
With this, QGroundControl will be running.

## PX4 Installation

The PX4 downloadLink: [https://docs.px4.io/main/en/ros2/user_guide.html](https://docs.px4.io/main/en/ros2/user_guide.html)

Make sure QGroundControl is running in the background (in a separate terminal).

In a new terminal:

```
pip install --user -U empy==3.3.4 pyros-genmsg setuptools
```

Setting up PX4 development environment
```
cd
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
```

To test if PX4 is downloaded properly, run the simulator below (will launch Gazebo drone/world)
```
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
cd PX4-Autopilot/
make px4_sitl gz_x500
```

With QGroundControl running, there should be no health status problems. To take off the drone to see if it works, in the PX4 terminal type:
```
commander takeoff
```

And the drone should take off! 

Additionally, from QGroundControl, it is possible to manually give set point commands to move the drone (to move to desired point/ rotate around fixed point). Commands from QGroundControl will be visible and executed in the Gazebo simulation. 

**Note**: For the installation process, stop here in the PX4 document: We don't download Micro XRCE-DDS Agent & Client because we work with MAVROS to communicate with the PX4 (Discussed next).

## MAVROS Installation

In a new terminal:

```
sudo apt install ros-humble-mavros ros-humble-mavros-extras
sudo apt install ros-humble-geographic-msgs
sudo apt install geographiclib-tools
sudo apt install libgeographic-dev
sudo apt install geographiclib-doc
```
Create the directories if they don't exist

```
sudo mkdir -p /usr/share/GeographicLib/geoids
sudo mkdir -p /usr/share/GeographicLib/gravity
sudo mkdir -p /usr/share/GeographicLib/magnetic
```

Install the specific egm96-5 dataset manually
```
sudo geographiclib-get-geoids egm96-5
```

With MAVROS, the PX4 running in a seperate terminal (see above) will connect to MAVROS via mavlink
```
source /opt/ros/humble/setup.bash
ros2 launch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
```