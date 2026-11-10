---
title: Ubuntu in VMware
author: Keith Currier, Max Gardenswartz
updated: 2026-11-06
status: draft
status_note: Moved from a PDF dated 2025-01-24. The steps are transcribed from it and have not been re-run by Max.
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  Runs on: Windows. How to install Ubuntu 22.04.5 in a VMware virtual machine on a Windows computer, so you can do the ROS 2 tutorials without deleting Windows. There is also a video walkthrough for VirtualBox: see Ubuntu in VirtualBox.
---

!!! note "Apple Silicon Macs Are Not Covered"
    There is no guide for Apple Silicon Macs, because they need an ARM-based Ubuntu. ROS 2 supports it, but some things, such as GPU acceleration for Gazebo, will not work. We have not tested these virtual machines with ROS on a Mac.

A virtual machine (VMware) lets you run Linux on your Windows computer without deleting the operating system. This guide gets Ubuntu running so you can do the ROS 2 tutorials. The same installation in VirtualBox, with a video, is on [Ubuntu in VirtualBox](ubuntu-in-virtualbox.md). The other software the lab uses is on [Software We Use](software-we-use.md).

!!! warning "Never Update Ubuntu"
    Use Ubuntu **22.04.5**, and do not update it. ROS 2 Humble needs it. When Ubuntu offers to upgrade, always decline.

## Install VMware

1. Download VMware Workstation Pro from the VMware link on [Software We Use](software-we-use.md). This guide used version 17. If it asks, use it for personal use.

2. Run the installer. The setup wizard is straightforward and needs no special changes.

    ![The VMware Workstation Pro 17 setup wizard welcome screen.](../images/tutorials/vm-vmware-setup.jpg){ width="60%" }

    One suggestion: turn off VMware checking for updates on startup, and update only when you open the Workstation.

3. Open VMware Workstation. The first time, it looks like this:

    ![The VMware Workstation Pro 17 home screen with Create a New Virtual Machine, Open a Virtual Machine, and Connect to a Remote Server.](../images/tutorials/vm-workstation-home.jpg){ width="70%" }

## Download Ubuntu

1. Download Ubuntu **22.04.5 LTS (Jammy Jellyfish)**, the **64-bit PC (AMD64) desktop image**. The file is called `ubuntu-22.04.5-desktop-amd64.iso` and lands in your downloads.

2. Move the file to a folder you will remember, so you know its path.

## Create the Virtual Machine

1. In VMware, choose **Create a New Virtual Machine**. Select **Installer disc image file (iso)** and give the path to the Ubuntu file. VMware should say that Ubuntu 64-bit 22.04.5 was detected.

    ![The New Virtual Machine Wizard with the installer disc image file selected and the message Ubuntu 64-bit 22.04.5 detected.](../images/tutorials/vm-new-vm-iso.jpg){ width="50%" }

2. Fill in your name, a username and a password for the virtual machine.

3. When it asks how large the disk should be, leave the standard size (20 GB) for just the ROS tutorials. If you need to flash NVIDIA Jetsons or do more with your VM, select 100 GB. Larger projects need more: see the note on disk space in [Software We Use](software-we-use.md#ubuntu).

    ![The New Virtual Machine Wizard disk capacity step with a maximum disk size of 20 GB.](../images/tutorials/vm-disk-size.jpg){ width="50%" }

4. Finish the wizard. The virtual machine boots, and the Ubuntu installer starts.

    ![The virtual machine, named Test_Ubuntu, starting up with the Ubuntu logo.](../images/tutorials/vm-ubuntu-boot.jpg){ width="70%" }

## Install Ubuntu

1. Use the standard settings. They are enough to learn ROS 2.

    ![The Ubuntu installer's Updates and other software step with Normal installation selected.](../images/tutorials/vm-install-updates.jpg){ width="70%" }

2. Ubuntu asks whether to erase the entire disk. This is fine here: the disk space belongs to the virtual machine, which you allocated already. Make sure you followed all the steps above and that Ubuntu is open in VMware Workstation, then start the installation.

    ![The Ubuntu installer's Installation type step with Erase disk and install Ubuntu selected, inside VMware Workstation.](../images/tutorials/vm-erase-disk.jpg){ width="70%" }

3. Enter your name, a computer name, a username and a password.

    ![The Ubuntu installer's Who are you step with empty fields for name, computer name, username and password.](../images/tutorials/vm-who-are-you.jpg){ width="60%" }

    Keep the computer name short and easy to remember, because you will see it in the terminal when you work in Linux and ROS 2. For example, if your name is Bob Murray, the computer name could be `bmurr`. Make the username and password easy to remember, since you use them to log in when the virtual machine starts or after it has been idle.

4. Let the installation continue. It restarts the virtual machine, then asks you to log in with the username and password you set. Continue the setup until you see the "You're ready to go" screen.

    ![The Ubuntu welcome screen saying You're ready to go, with a row of suggested apps.](../images/tutorials/vm-ready-to-go.jpg){ width="60%" }

5. Ubuntu will prompt you to update. **Do not update.** Click **Don't Upgrade**. Keep Ubuntu 22.04.5 to work on ROS 2 Humble.

    ![Two Ubuntu pop-ups, an upgrade to Ubuntu 24.04.1 LTS with the Don't Upgrade button underlined, and a Software Updater window.](../images/tutorials/vm-dont-upgrade.jpg){ width="70%" }

6. Ubuntu is now fully installed. Add the terminal to your favorites so it stays on the taskbar: click **Show Applications** at the bottom of the taskbar, then right-click the terminal and favorite it.

    ![The Ubuntu application grid with the Show Applications button circled and a message that Terminal has been added to your favorites.](../images/tutorials/vm-favorite-terminal.jpg){ width="70%" }

## Next: ROS 2

Open the terminal and install ROS 2 by following the official Humble guide. A video walkthrough is on [Software We Use](software-we-use.md#ros-2-humble). Then do the tutorials.

[ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html){ .md-button }
[ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html){ .md-button }
