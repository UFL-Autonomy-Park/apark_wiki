# Indoor Lab Networking Setup

Our lab's LAN is not connected to the Internet, so each computer needs a special netplan file such that all DNS traffic goes to UF but all robot traffic stays on our private LAN. Our LAN has a WiFi component. While it can be joined, this is only for robots (unless you have two WiFi cards somehow).

### Route DDS Traffic Through Robot Network

!!! note
    **ALL USERS ON THE NCR COMPUTERS WILL NEED TO PERFORM THIS STEP. OTHERWISE YOUR NODES WILL NOT WORK.**

To get all ROS traffic to be routed through the robot network run
```
sudo nano uf_fastdds_profile.xml
```
and paste the following code:
```
<?xml version="1.0" encoding="UTF-8" ?>
<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">

    <transport_descriptors>
        <transport_descriptor>
            <transport_id>MyRobotUDPTransport</transport_id>
            <type>UDPv4</type>
            <interfaceWhiteList>
                <address>192.168.1.100</address>
            </interfaceWhiteList>
            </transport_descriptor>
    </transport_descriptors>

    <participant profile_name="ParticipantUsingRobotUDP" is_default_profile="true">
        <rtps>
            <useBuiltinTransports>false</useBuiltinTransports> <userTransports>
                <transport_id>MyRobotUDPTransport</transport_id> </userTransports>
        </rtps>
    </participant>

</profiles>
```
Lastly, set the following environment variables in `.bashrc`
```
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export FASTRTPS_DEFAULT_PROFILES_FILE=/home/$USERNAME@ad.ufl.edu/uf_fastdds_profile.xml
```
Open a new terminal and run your ROS nodes without any networking issues!

### Route DNS Traffic Through UF Network

!!! warning
    **ONLY PERFORM THE FOLLOWING STEPS IF YOU ARE SETTING UP THE COMPUTER OR SOMETHING WITH THE NETWORK IS BROKEN.**

To make everything work properly, we use the following `netplan` file. Run `sudo nano /etc/netplan/01-network-manager-all.yaml` and paste the following. This example is for the computer under IP 192.168.1.201 (MAE-BPLJHL2).

You will need to know the device name for your Ethernet (used for robots/LAN) and wireless/WiFi adapater (all computers have a built-in card for it) from `ifconfig`.
```
network:
  version: 2
  renderer: NetworkManager 
  ethernets:
    enp0s31f6: # Ethernet interface. Replace with your computer's unique name
      dhcp4: true # Let the Ubiquiti router dictate the IP (should be staticly assigned in the Ubiquiti portal)
      dhcp4-overrides: # Ubiquiti will try and also serve a DNS and default gateway with this local IP. Disable.
        use-routes: false
        use-dns: false
```
After saving, run `sudo netplan apply`. 

Log in to eduroam (or use ufgetonline's script). If logging in, select "No certificate is required" then select the domain as "ufl.edu" but be sure to still use "@ufl.edu" when typing your UF username and password.

## super_client_config.xml

I know you forgot this somewhere. Grab it a fresh one from the ROS 2 tutorial page on this. If one space is off, it may not work!

```
<?xml version="1.0" encoding="UTF-8" ?>
<dds>
    <profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">
        <participant profile_name="super_client_profile" is_default_profile="true">
            <rtps>
                <builtin>
                    <discovery_config>
                        <discoveryProtocol>SUPER_CLIENT</discoveryProtocol>
                        <discoveryServersList>
                            <RemoteServer prefix="44.53.00.5f.45.50.52.4f.53.49.4d.41">
                                <metatrafficUnicastLocatorList>
                                    <locator>
                                        <udpv4>
                                            <address>192.168.1.201</address>
                                            <port>11811</port>
                                        </udpv4>
                                    </locator>
                                </metatrafficUnicastLocatorList>
                            </RemoteServer>
                        </discoveryServersList>
                    </discovery_config>
                </builtin>
            </rtps>
        </participant>
    </profiles>
</dds>
```

## Add to .bashrc

```
source /opt/ros/humble/setup.sh
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DISCOVERY_SERVER=192.168.1.201:11811
export FASTRTPS_DEFAULT_PROFILES_FILE=~/super_client_config.xml
```
