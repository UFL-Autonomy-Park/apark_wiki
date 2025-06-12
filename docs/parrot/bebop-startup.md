---
title: NCR Lab Bebop Minimal Startup
---

The `ncr_bebop` repo on the Gitea server contains all of the necessary packages for a minimal startup, joy control, and setpoint control for the Parrot Bebop 2 drones in the NCR lab. To build all packages and install the ROS2 driver for the Bebop, follow the instructions in the [ROS 2 Bebop Autonomy (Driver Support)](../parrot/ros2-bebop.md) guide.

Typically, you will need to build `ros2_parrot_arsdk` followed by `ros2_bebop_driver`, and then you can build `bebop_teleop`. In the `bebop_teleop` package, make sure that the namespace is correct for the Bebop you are using.

To run the packages in the `ncr_bebop` repo do `cd ncr_bebop && source install/setup.bash`. Then, open four separate terminals and run
```
# Run joy (make sure PS4 Dualshock controller is connected)
ros2 run joy joy_node
```
```
# Run Bebop driver
ros2 launch ros2_bebop_driver bebop_node_launch.xml ip:=YOUR.BEBOP.IP.ADDRESS 
```
```
# Mocap topics
ros2 launch vrpn_mocap client.launch.yaml server:=192.168.1.202 port:=3883 
```
```
# Teleop node
ros2 run bebop_teleop joy_cmd_node
```

Once all nodes are running and the Bebop is connected, press the PS button to take off. A subsequent press of the PS button will land the Bebop. To switch to setpoint mode, press X. Only do this if you have confirmed that position feedback for your Bebop is available. 