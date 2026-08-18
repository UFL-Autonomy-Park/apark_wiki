# Flying Quadcopters

## 0.0 QUICK REFERENCE
The slide deck for this SOP can be found [here](../SOPs/quadcopter-sop.pdf)

### 0.1 Pre-Flight
1. Fill out the [pre-flight form](https://forms.cloud.microsoft/r/em7Rd03Vnq) before ANY operations take place
2. Ensure all operators are wearing pants, closed-toed shoes, eye protection, and have tied back long hair
3. The POC/RPIC should ensure that at least two fully charged batteries are readily available
4. Check the NWS forecast or other official source to ensure that there is no precipitation or sustained wind speeds over 15 mph (~7 m/s)
5. DO NOT POWER A QUADCOPTER OUTSIDE OF A NETTED FACILITY UNLESS THE PROPELLERS HAVE BEEN REMOVED

### 0.2 In-Flight
1. RPIC must have hands on the remote controller at all times during flight
2. RPIC and VO must have quadcopter within their VLOS at all times during flight
3. Never conduct aerobatics
4. NEVER FLY A QUADCOPTER WITH A PERSON INSIDE OF A NETTED FACILITY

### 0.3 Post-Flight
1. Disarm the quadcopter immediately after landing
2. RPIC or VO enter the netted facility to quickly disable power from the quadcopter, while the other has hands on the remote controller to prevent accidental arming

### 0.4 Emergencies
1. If damage occurs to equipment, contact your PI.
2. If an injury occurs, call 911 if is life threatening or serious. If it is not serious, apply first aid. Contact your PI ASAP. If medical attention is required, get in touch with AmeriSys at 1-800-455-2079. 

## 1.0 PURPOSE
This document provides information pertaining to the safe piloted and autonomous operation of quadcopters at the University of Florida (UF) Autonomy Park, the Systems, Cognition, and Control (SCC) Laboratory, and the Nonlinear Controls and Robotics (NCR) Laboratory.

## 2.0 SCOPE/APPLICABILITY
The procedures and protocols apply to any member of the University of Florida Herbert Wertheim College of Engineering who plan to operate quadcopters, or will be in the field with quadcopters.

## 3.0 TERMS, DEFINITIONS, AND ABBREVIATIONS
**AGL**:
Above Ground Level. 

**Controller**:
An algorithm which uses feedback and/or data to autonomously stabilize a system or accomplish an objective. Distinct from a "remote controller," which is a tool used to send remote signals to a robot/quadcopter.

**LiPo**:
Lithium-ion polymer battery. Instead of a liquid electrolyte, LiPos typically use a gelled or solid polymer-based electrolyte as the conductive medium.

**MAVLink**:
[MAVLink](https://en.wikipedia.org/wiki/MAVLink) is a protocol for communicating with small unmanned vehicles.

**MAVROS**:
[MAVROS](https://github.com/mavlink/mavros) is an interface which routes MAVLink messages to and from ROS 2, allowing for autonomous control of quadcopters over the air. 

**METAR**:
METeorological Aerodrome Report. International standard for hourly aviation weather reports.

**POC**:
Person Operating Controls. Refers to the individual using a remote controller to pilot the quadcopter

**PX4**:
[PX4](https://px4.io/) is an open source flight control software for drones and other unmanned vehicles. 

**QGC**:
[QGroundControl](https://qgroundcontrol.com/) (QGC) is a computer program which provides full flight control and vehicle setup for PX4 or ArduPilot powered vehicles.

**RC**:
Remote control. Indicates a physical remote which sends commands (takeoff, land, roll, pitch, yaw) to a quadcopter using radio communication. 

**ROS**:
[Robot Operating System](https://docs.ros.org/en/humble/index.html) (ROS) is a middleware which facilitates communication between computers, robots, and other hardware using a standardized protocol and message format.

**RPIC**:
Remote Pilot In Command. Refers to the individual responsible for the autonomous code running on the quadcopter, and associated failsafes 

**TAF**:
Terminal Aerodrome Forecast. 

**UAS**:
Unmanned Aerial System. Examples include quadcopters and fixed-wing aircraft without pilots on board.

**VLOS**:
Visual Line of Sight. 

**VO**:
Visual Observer. Refers to the individual who acts as a "second set of eyes" during flight operations.

## 4.0 QUADCOPTERS
### 4.1 Platforms
The Herbert Wertheim College of Engineering owns and operates a fleet of more than 20 quadcopters at the UF [Autonomy Park](https://mae.ufl.edu/research/facilities/autonomy-park/) (Drone Support Bldg 1, Drone Support Bldg 2, and netted facility). These quadcopters include:
- 3x [Freefly Astro](https://docs.freeflysystems.com/astro)
- 1x [Freefly Alta X](https://docs.freeflysystems.com/products/products/alta-x)
- 20x ["Homebrew" Quadcopters](https://autonomypark.org/homebrew/diy-drone/)

The Freefly Astro is a quadcopter designed by Freefly Systems for enterprise and industrial applications (e.g. cinematography, surveying/mapping, industrial inspections). External connectivity is handled via radio to the [Herelink remote controller](https://docs.cubepilot.org/user-guides/herelink/herelink-overview) or via WiFi to the onboard computer. The Astro has a maximum payload of 1500g. 

The Freefly Alta X is a heavy-lift quadcopter design by Freefly Systems for professional multi-rotor aircraft designed for demanding cinematic, professional, and industrial applications. The Alta X is a demanding platform that can cause serious injury to people and property. As such, the Alta X should not be operated without extensive training. External connectivity is handled via radio to the [Futaba T14SG](https://futabausa.com/product/14sg/) remote controller, via radio to the ground station (computer) using the provided USB-C dongle, and via WiFi using a mounted Jetson Orin Nano. The Freefly Alta X has a maximum payload of 15000g. 

The "Homebrew" quadcopters refer to a fleet of quadcopters whose components were specifically selected to facilitate research of autonomous control algorithms of multi-agent aerial systems. A detailed parts list can be found on the [Autonomy Park Wiki](https://autonomypark.org/).

The SCC/NCR research groups utilize 10x [Parrot Bebop 2](https://en.wikipedia.org/wiki/Parrot_Bebop) quadcopters for use in the indoor lab facility in MAE-A 313. The Bebops can be controlled via WiFi using a ground station running ROS2. 

### 4.2 Methods of Operation
Quadcopter operations fall into two major domains: piloted and autonomous flights. For the purposes of this document, "piloted flight" will encompass all operations using a quadcopter which are conducted by a human pilot using a remote control whose commands are executed using the quadcopter's **onboard** control algorithms. "Autonomous flight" encompasses all remote operations which require the drone to enter an "offboard" state, in which external velocity or acceleration commands are delivered to the quadcopter. This includes teleoperation of a quadcopter whose commands are facilitated though ROS2 and a user-design autonomous control algorithm.

## 5.0 MISSION PLANNING
Quadcopters should only be flown for supervised flight practice, or with an explicit research purpose in mind. Recreational use of UF-owned quadcopters is not permitted. As such, each use should be carefully planned. Each mission or experiment plan should be able to be quickly summarized in the following fields:
```
1. Date of flight:
2. Flight duration (hours, total operation time):
3. Quadcopter(s) in use:
4. Purpose of flight:
5. Person operating controls (POC)/ Remote pilot in command (RPIC):
6. Visual observer (VO): 
```
The answers to the queries above should be filled out on the attached [form](https://forms.cloud.microsoft/r/em7Rd03Vnq) BEFORE EACH FLIGHT.

## 6.0 PRE-FLIGHT OPERATIONS
The following procedures should be conducted before any piloted or autonomous operation of a quadcopter.

### 6.1 Lab Attire/Personal Protective Equipment (PPE)
You are in violation of UF lab safety protocols if you enter the Autonomy Park or indoor lab without closed-toed shoes, long pants, and a shirt with adequate coverage. You also must wear eye protection when in the indoor lab or Autonomy Park, and especially while conducting a quadcopter flight. 

### 6.2 Batteries and Charging
LiPo and Li-Ion batteries can experience thermal runaway during charging, which can lead to fire. See the [LiPo Standard Operating Procedure](https://autonomypark.org/SOPs/batteries/) for best practices regarding battery charging, use, and maintenance. We emphasize that quadcopter batteries should not be left unattended while charging.

Each quadcopter accepts a different type of battery with a different charging protocol. See your quadcopter's manual for exact specifications. Before each flight, the POC/RPIC should ensure that at least two fully charged batteries are readily available for the quadcopter being operated. Flight should only be conducted using fully charged batteries. 

### 6.3 Weather
Weather is one of the largest variables in quadcopter flight, especially in Florida. The FAA heavily discourages flight operations in precipitation, and we concur. All quadcopters are grounded in the event of rain. This protects both the equipment (which is expensive, our quadcopters are not IP rated) and the operator (in case of emergency, precipitation complicates execution of protocols). 

Wind represents the most common weather limitation for drone operations. Most consumer and commercial drones have maximum wind speed tolerances ranging from 20-35 mph (~9-16 m/s), though operational limits should be more conservative than manufacturer specifications. Generally limit operations to 15-20 mph (~7-9 m/s) for safe control. An estimate of the current wind speed at the Autonomy Park can be obtained from the anemometer via Home Assistant, or, in the case that the anemometer is malfunctioning, from the [NWS forecast](https://forecast.weather.gov/MapClick.php?CityName=Gainesville&state=FL&site=JAX&textField1=29.6742&textField2=-82.3363&e=0) which reports the wind speed at the Gainesville Regional Airport (KGNV). 

For detailed hourly conditions at KGNV as well as the aviation forecast, the METAR and TAF can be obtained [here](https://aviationweather.gov/data/metar/?ids=KGNV&taf=1). 

If Starlink is to be used for remote operations, ensure that there is minimal cloud cover to reduce latency.

### 6.4 Quadcopter Setup
No quadcopter should EVER be powered outside the netted facility at the Autonomy Park, or in a region of the indoor lab which contains individuals not protected by a net. Moreover, no quadcopter battery should be installed outside the netted facility unless the quadcopter is fastened to the ground and the area around the quadcopter is secured, as powering the quadcopter provides the potential for flight.

In the event that the quadcopter must be brought indoors (software update, hardware maintenance, or similar troubleshooting), the propellers of the quadcopter should be removed before powering the quadcopter and bringing it indoors. Ensure the quadcopter's battery is not installed when removing the propellers. Note that the quadcopter motors always have the potential to rotate rapidly, and can cause damage to loose hair or clothing. Hair should be tied back to prevent entanglement and loose clothing should be secured or removed, i.e., tuck long/loose shirts in. 

During normal operations, move the quadcopter into the netted facility. If at the Autonomy Park, bring a walkie talkie so you may communicate with the RPIC or VO. If using the Astro or Alta X, unfold the propeller arms, lock the arms out, and spread the propellers so they are not touching one other. All quadcopters should be placed at least 9 ft (~3 m) from any net if outdoors and at least 3 ft (~1 m) from any wall or net if indoors. Once the quadcopter is in its takeoff position, insert the battery. Ensure the battery is firmly seated. When the battery is seated, plug the drone in to power it on. Powering the drone should be your last task inside the netted facility and you should have a clear path to the exit. Leave the netted facility and close it appropriately. 

### 6.5 Wireless Connectivity
The RPIC and VO should ensure that there is little to no latency when communicating with the quadcopter (either over radio for piloted flight, or WiFi for autonomous flight) prior to takeoff. On the Astro, should navigate to the "Vehicle Overview" menu, and select the "Connectivity" tab to ensure the quadcopter is connected to `UFLAutonomyPark_5GHz`. On all other wifi-enabled quadcopters, the quality of connection should be verified on the Unifi dashboard at `192.168.1.1` under the "Client Devices" menu. Prior to autonomous flight, the quality of data transmission for critical ROS topics should also be verified using the `ros2 topic hz /your_topic_name` command. 

## 7.0 PILOTED FLIGHT PROCEDURES
This section discusses best practices for piloted flight of quadcopters at the Autonomy Park. The quadcopters in the SCC/NCR lab, in their current configuration, can only be controlled in an offboard configuration using ROS2 and will thus not be discussed in this section. 

The descriptions of the manual, position, and altitude mode are sourced from the [Freefly Docs](https://docs.freeflysystems.com/astro/pilots-operating-handbook/flight-part-1-flight-modes).

### 7.1 Non-Negotiables
1. The RPIC should always have their hands on the controller when flying a quadcopter.
2. The RPIC must have the quadcopter within their VLOS at all times.
3. The RPIC must never perform aerobatics with the quadcopter.
4. NO QUADCOPTER OPERATIONS MAY EVER BE CONDUCTED WHILE A PERSON IS INSIDE OF THE NETTED FACILITY.

### 7.2 Takeoff
Ensure no people are in netted facility and it has been closed using the provided carabiners. You can either use the provided PX4 autonomous takeoff protocol, which will then place the drone into a loiter state after a successful takeoff, or do it yourself. The PX4 takeoff will cause the drone to rise ~9 ft (2.5 m) AGL. After manual takeoff, switch into your desired flight mode. NEVER MANUALLY TAKE OFF IN POSITION OR ALTITUDE MODE. THE QUADCOPTER HAS BEEN KNOWN TO TIP OVER IN THESE STATES. 

### 7.3 Manual Mode
Any RPIC should be qualified to pilot the quadcopter in manual mode. This skill can be honed virtually in the [Liftoff](https://www.liftoff-game.com/) simulation using a real RC transmitter on the "Steve" computer in the indoor lab space. 

In Manual Mode, when the pitch and roll stick is centered, the aircraft will attempt to remain level and will drift with the wind. The aircraft will require constant throttle adjustment to hold altitude.

In Manual Mode, the pitch and roll stick controls the aircraft angle. The further upward the pitch stick, the further the quadcopter will tilt forward. When the pitch stick is pulled downward, the quadcopter will tilt backward. Similarly, for roll in the left and right directions. Lateral speed is not controlled by the autopilot.

The throttle stick controls motor speed directly. Deflecting the throttle stick left and right controls the yaw rate. The speed of yaw rotation is proportional to stick deflection.

### 7.4 Position Mode
In Position Mode, when the sticks are centered, the quadcopter will maintain its position over a point on the ground and maintain altitude, correcting for disturbances.

In Position Mode, the pitch/roll stick commands the speed of the drone relative to the ground. The further upward the pitch/roll stick, the faster the quadcopter will fly forward. When the pitch/roll stick is pulled downward, the quadcopter will fly backward. Similarly, the pitch/roll stick will move the quadcopter in the left and right directions when moved to the left and right.

The throttle stick commands vertical speed. The further upward the throttle stick, the faster the quadcopter will climb. Conversely, the lower the throttle stick position, the faster the quadcopter will descend. Deflecting the throttle stick left and right controls the yaw rate, with the speed of rotation proportional to stick deflection.

### 7.5 Altitude Mode
Similar to Position mode, the pitch/roll stick moves the quadcopter laterally relative to the ground and the throttle stick commands vertical speed and yaw. However, while the drone can hold its vertical position using the barometer, lateral speed is not controlled by the autopilot in Altitude mode. The quadcopter will drift with the wind, will not stop immediately after lateral movement, and will probably not hold a single point above the ground without pilot input. 

### 7.6 Landing
The landing area of the quadcopter should be flat, clear of any debris, and at least 3m away from any net or wall if outdoors, and at least 1m clear of any net or wall if indoors. If you are flying in position mode and the drone is in a stable hovering state, you may use the autonomous landing protocol designed by PX4. Otherwise, bring the quadcopter to the ground gently by lowering the throttle until all landing gear have made contact with the ground. Then, reduce the throttle to zero and DISARM THE QUADCOPTER. This landing procedure can be performed in Manual, Position, and Altitude mode. 

## 8.0 AUTONOMOUS FLIGHT PROCEDURES
### 8.1 Offboard Mode
Offboard mode is inherently the most dangerous operating condition for any quadcopter. You are handing over the wheel to an autonomous algorithm that is (in our case) experimental/cutting edge. EXTREME PRECAUTIONS MUST BE TAKEN IN THIS MODE. To prevent damage to property or injury to individuals, any code written to be deployed on the quadcopters should be THOROUGHLY vetted in our PX4 simulation environment. We have curated a "digital twin" environment, which even models the geometry of the Autonomy Park netted facility. 

Note that on PX4-enabled quadcopters, offboard mode can be overridden by sending any RC command. The quadcopter will then enter postion mode, enabling the RPIC to safely pilot the quadcopter to the home location if something goes wrong while in offboard mode. 

### 8.2 Return to Home Mode
This flight mode is only present on PX4-enabled quadcopters and does not pertain to the Parrot Bebops. In this mode, the quadcopter will abandon its active command/mode, fly to a predefined altitude, and fly itself back to the GPS coordinates at which it took off. If your quadcopter does not have obstacle avoidance enabled, it will run into obstacles on its way home. We recommend to never use this mode unless in dire circumstances (i.e., as a failsafe). The default parameter causes the quadcopter to rise to 60m before returning home. This will (obviously) cause the quadcopter to shoot up vertically into the top net. To avoid this, ensure the following parameters are set before flight:
```
RTL_RETURN_ALT = 2.5 M
RTL_DESCEND_ALT = 2.5 M
```
Additionally, in the "Safety" settings, make sure that all RTL and takeoff altitudes are not greater than ~9 ft (2.5 m). 

### 8.3 ROS 2 Code
When writing packages for PX4-enabled quadcopters at the Autonomy Park, NEVER "roll your own" flight stack (e.g., rig up a takeoff, landing, offboard mode switcher + coordinate transformations). The [aero-common](https://github.com/UFL-Autonomy-Park/aero_common) package has been carefully designed to ensure consistency in all quadcopter autonomous operations.

## 9.0 POST-FLIGHT OPERATIONS
The drone should be disarmed as soon as it lands. If another operation/experiment run is planned within a short duration and the battery percentage is adequately high (>50%), leave the drone in the netted facility powered on (i.e., in the disarmed state with the battery still installed).

No operator should enter the net if more experiments will be conducted. The only appropriate time for an operator to enter the netted facility containing quadcopters with batteries installed is after the conclusion of an experiment, and for the sole purpose of disconnecting the battery. When an operator enters the net, they must have a walkie-talkie on their person to communicate with the RPIC/VO who is inside the shed. The RPIC/VO should ensure that all methods of controlling the drone (e.g. Herelink remote and any ROS terminals) are secured and prevented from sending any accidental takeoff commands. Prior to the operator approaching the quadcopter, the RPIC/VO must verbally confirm that the quadcopter is in a Disarmed state. 

## 10.0 MULTI-AGENT OPERATIONS
This section of the SOP is under development.

## 11.0 EMERGENCY PROCEDURES
Research involving quadcopters is inherently dangerous and subject to mission failure in a variety of ways.

### 11.1 Loss of Feedback
In the case of piloted or autonomous flight, loss of feedback can lead to unstable quadcopter behavior (e.g. uncontrolled flight into obstacles or the ground), or an inability to land the quadcopter. In the event that feedback is lost via ROS or via radio, the drone failsafe (PX4 parameters `COM_OBL_RC_ACT` or `COM_OF_LOSS_T`) should activate, causing the drone to either land or loiter, depending on how the drone has been configured by the user. 

If the failsafe does not engage and the drone is in a safe, hovering state, the user should take over command using the remote control and land the drone safely. If the remote control will not engage, the VO should attempt to restart the MAVROS telemetry node and send a landing command using the Xbox controller. 

### 11.2 Loss of Control
In the event of total loss of control (i.e., catastrophic failure in which the onboard computer cannot be reached and the RC controller will not send commands), the operators must let the quadcopter exhaust its battery and land (the `COM_FAIL_ACT_T` should be set to land mode), or, unfortunately, crash. During this period the quadcopter should be kept within VLOS and attempts should be made to reconnect with the quadcopter by restarting remote controls and ROS nodes, but NO PERSON SHOULD ENTER THE NET WHILE THE QUADCOPTER IS IN FLIGHT. 

In the event of a full crash, the drone must be safely disarmed and the battery must be disconnected/removed. The period after a crash represents the highest likelihood of flight crew injury and must be taken seriously. The blades of the quadcopter may still spin, causing unexpected motion, even after a catastrophic crash. The RPIC must DISARM the drone or flip the KILL SWITCH on the RC before anyone enters the netted facility to power down the drone.

The operator entering the netted facility must be wearing appropriate PPE, including gloves to protect their hands. No operator should approach a "live" quadcopter that cannot be confirmed to be disarmed. In the case that the quadcopter cannot be confirmed to be disarmed, the "drone recovery kit" consisting of a moving blanket, leather gloves, and a long sleeve smock should be used to physically disable the drone. The blanket should be used to ensure that the propellers cannot rotate, preventing flight. Approach the drone carefully and quickly. Never reach over the travel path of the propellers. Quickly pull the power or battery and DO NOT ATTEMPT TO DIAGNOSE THE HARDWARE BEFORE POWER HAS BEEN DISENGAGED. 

## 12.0 ACCIDENTS AND INJURIES
In the case of an incident involving only equipment (e.g., the quadcopter crashes inside of the netted facility and the landing gear is damaged, but no people are harmed), report the incident to your PI. 

In the case of an accident involving physical injury, CALL 911 IF THE INJURY IS SERIOUS OR LIFE-THREATENING, and get medical attention ASAP. If the injury is not serious, apply first aid. If the injury requires medical attention, call AmeriSys at 1-800-455-2079 before consultation with a medical professional. Once the injury has been treated or emergency personnel have arrived, contact your PI to notify them of the incident and report the accident to [UF Environmental Health & Safety](https://apps.ehs.ufl.edu/incidents).