# Autonomy Park File Share

This will allow you to access all of our shared Autonomy Park files in the TrueNAS file share which has 192 TB of storage.

!!! note
    The tutorial below for Linux is for accessing the drive via the NFS protocol, while the Windows and macOS ones use SMB. **Both access the same data.**

### Preliminaries

First, you must be connected to the Autonomy Park LAN by physically being at the park or connecting to it via ZeroTier.

### Linux
In terminal, run

```
mkdir /home/$USER/uflautonomypark
sudo mount -t nfs "192.168.1.32:/mnt/Autonomy Park/uflautonomypark" /home/$USER/uflautonomypark/
```

Then, to keep from re-mounting every time you reboot, run

```
sudo nano /etc/fstab
```

and add this at the end of the file

```
192.168.1.32:/mnt/Autonomy\040Park/uflautonomypark /home/$USER/uflautonomypark nfs defaults,_netdev 0 0
```

Save with **Ctrl-S** and exit with **Ctrl-X**. You may now transfer files to and from the NAS.

To unmount the drive when not in use, run

```
sudo umount /home/$USER/uflautonomypark
```

### Windows

Open any version of Powershell (**not** Command Prompt) and run the following command.

```
net use Q: \\192.168.1.32\uflautonomypark /user:TRUENAS\autonomypark $PASSWORD /persistent:yes
```

where the `$PASSWORD` must be given to you by an admin. You may now transfer files to and from the NAS.

!!! note
    Do **not** try and manually add the SMB share drive manually through File Explorer. It is not possible.

To remove the virtual drive, right click on it in File Explorer and click "Disconnect".


### macOS

Open Finder. Select Network in the left sidebar. (If Network doesn't appear because you've customized Finder, go to your Mac's name under "Locations" and you'll find it there.) A folder called "truenas" will appear. Double click on it. It may take a moment to load, but you will soon see a folder called "uflautonomypark". This will connect you as a guest, but guest access will be disabled by default for security reasons so you will not be able to access anything yet. Click "Connect As." It may take a moment to load. Fill out the pop-out that appears as follows:

* **Connect As:** Select **Registered User**.
* **Name:** Enter `TRUENAS\autonomypark`.
* **Password:** Enter the password. (Ask an admin.)
* **Remember this password in my keychain:** Check this box.

Click "Connect." It may take a while to load. Double click on the "uflautonomypark" folder. You may now transfer files to and from the NAS.

!!! note
    On macOS, this virtual drive connecting you to the NAS will unmount automatically every time you log out. You will have to go back to Finder and remount. If you saved your login, double clicking the folder will get you back. Of course, connect to ZeroTier first.

!!! note    
    On macOS, the virtual NAS drive folder will remain mounted even when you disconnect from ZeroTier, but, expectedly, you will not be able to access files. It's easy to get confused.

### Large File Transfers

Be careful walking away from large file transfers. Sometimes, failures to complete a large file transfer (> 5GB) will not raise error messages. This is important especially if you have a lot of small files that cumulatively have a large size. Verify that the sizes and number of files of the copied data and your local copy match for important transfers!