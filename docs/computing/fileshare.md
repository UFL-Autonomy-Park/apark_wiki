# Autonomy Park File Share

Add the TrueNAS file share to your Ubuntu computer. This will allow you to access all of our shared Autonomy Park files

```
mkdir /home/YOURUSERNAME/uflautonomypark
sudo mount -t nfs "192.168.1.32:/mnt/Autonomy Park/uflautonomypark" /home/YOURUSERNAME/uflautonomypark/
```

Then, to keep from re-mounting every time you reboot, run the following command

```
sudo nano /etc/fstab
```

and add this at the end of the file:

```
192.168.1.32:/mnt/Autonomy\040Park/uflautonomypark /home/YOURUSERNAME/uflautonomypark nfs defaults,_netdev 0 0
```

To unmount, run

```
sudo umount /home/YOURUSERNAME/uflautonomypark
```
