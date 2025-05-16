---
title: ZeroTier VPN Install
---

We use [ZeroTier](https://www.zerotier.com/download/#linux) to connect remotely to Autonomy Park assets (computers, robots, etc.). ZeroTier is one of the few VPN services that allows for multicast, which lets us publish and subscribe to ROS topics when we are not at the park. 

To install ZeroTier, run
```
curl -s https://install.zerotier.com | sudo bash
```

Once ZeroTier is installed, run `systemctl status zerotier-one` to ensure that ZeroTier is running. If it is not running, enter the command `sudo systemctl start zerotier-one`. Next, connect the Autonomy Park network. Run 
```
sudo zerotier-cli join $NETWORK
```
where `$NETWORK` is the placeholder for the Autonomy Park network ID. It should return `200 join OK`. The network ID can be found on the ZeroTier dashboard. **Do not share this network ID.** 

Once you successfully join the network, navigate to the ZeroTier dashboard on the web and find the member that joined most recently. Click the "Edit" button, name your computer (be descriptive). Thne, check the selection box and click "Authorize". 

!!! warning
    If your local network uses the subnet `192.168.1.XXX` you will run into IP conflicts. We are working on changing this. 

Congrats! You are now connected to the Autonomy Park. When you wish to connect/disconnect from ZeroTier, run `sudo systemctl start zerotier-one` or `sudo systemctl stop zerotier-one`, respectively.