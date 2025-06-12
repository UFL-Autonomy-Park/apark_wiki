# Basic Reference

## HAVE YOU DONE THE ROS 2 TUTORIALS YET?

<a href="https://docs.ros.org/en/humble/Tutorials.html" target="_blank">Get on it, soldier</a>

If you are trying to do the ROS tutorials in a VM, see Keith's setup guide [here](../ROS/vmware-guide.pdf)


## ROS 2 Humble Install

<iframe width="560" height="315" src="https://www.youtube.com/embed/tvToTLZQkZI?si=97aXUDweP7OQRK9T" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## NCR Battlestation Config
The main computer in the NCR lab is managed by UFIT. As such, there are some more hoops we need to jump through. We have two ethernet interfaces. The interface `enp0s31f6` is for the UF network and is required for authentication and `sudo`. The interface `enp4s0` is for our local network where all of the robots live. 

### Route DDS Traffic Through Robot Network

!!! note
    **ALL NEW USERS ON THE NCR BATTLESTATION WILL NEED TO PERFORM THIS STEP. OTHERWISE YOUR NODES WILL NOT WORK.**

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

To make everything work properly, we use the following `netplan` file. Run `sudo nano /etc/netplan/01-network-manager-all.yaml` and paste the following:
```
network:
  version: 2
  renderer: NetworkManager 
  ethernets:
    enp0s31f6: # Your UF Network Interface
      dhcp4: true
      dhcp4-overrides:
        route-metric: 100 # Explicitly set good metric for UF
        use-dns: true # Ensure it uses UF DNS
    enp4s0: # Your Robot Network Interface
      dhcp4: true
      dhcp4-overrides:
        use-routes: false # <--- ADD THIS LINE or ensure it's false
        # You might also want to prevent it from setting DNS if the robot network's DHCP provides one
        use-dns: false # <--- ADD THIS LINE if you only want UF DNS
        # If you absolutely needed a route from it but NOT default, you could give it a high metric:
        # route-metric: 500

```

After saving, run `sudo netplan apply`. 


## super_client_config.xml

I know you forgot this somewhere

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
