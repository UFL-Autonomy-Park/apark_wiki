---
title: New Jetson Setup w/ CUDA, Zed SDK
---

```
# THIS WILL ONLY WORK FOR JETPACK 6.0 WITH CUDA 12.2
# WILL ADD ADDITIONAL INFO FOR MAVROS

sudo apt update && sudo apt upgrade

# Wi-Fi
sudo nmcli device wifi connect "UFLAutonomyPark_5GHz" password "43PrismaticJackalsAte10Huskies!"

# install terminator
sudo apt-get install terminator

# install onnx
pip install onnx

# install nano
sudo apt-get install nano

# change hostname
sudo hostnamectl set-hostname new-hostname

# update /etc/hosts
sudo nano /etc/hosts
sudo reboot # unplug the ethernet cable at this point

# install jetsonUtilities - MAKE SURE CUDA IS INSTALLED
git clone https://github.com/jetsonhacks/jetsonUtilities.git
cd jetsonUtilities
./jetsonInfo.py
cd ..

# download zed sdk
wget -q --no-check-certificate -O ZED_SDK_Linux.run https://download.stereolabs.com/zedsdk/4.2/l4t36.3/jetsons
chmod +x ZED_SDK_Linux.run
./ZED_SDK_Linux.run 
sudo rm -rf /usr/local/zed/resources/*
sudo rm -rf ZED_SDK_Linux.run
sudo rm -rf /var/lib/apt/lists/

# locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# verify
locale 

# install ros2 and dev tools
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update && sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
echo "source /opt/ros/humble/setup.sh" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=2" >> ~/.bashrc
source ~/.bashrc

# set up rosdep
sudo rosdep init
rosdep update

# install zed_ros2_wrapper
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone --recurse-submodules https://github.com/stereolabs/zed-ros2-wrapper.git
cd ..
sudo apt update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
echo source $(pwd)/install/local_setup.bash >> ~/.bashrc
source ~/.bashrc

# install zed-ros2-examples
cd ~/ros2_ws/src/ 
git clone https://github.com/stereolabs/zed-ros2-examples.git
cd ..
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
source ~/.bashrc

# start a zed node
# on first launch the AI model needs to be optimized, it will take a bit
# NO DASHES IN CAMERA NAME!
ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2i camera_name:=ncr_zed

# open another terminal to visualize the data
ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2i
```