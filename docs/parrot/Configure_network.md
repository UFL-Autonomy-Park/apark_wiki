# Configuring the WiFi on Bebops

This guide shows how to configure the network and IP on Bebop2 and how to add that script to boot so that the IP does not need to be manually set every use.

## Step 1: Clone GitHub Repository and Edit `shortpress_3.sh` File
1. **Clone the repository from GitHub:**
```
git clone https://github.com/tnaegeli/multiple_bebops.git
```
2.  **Navigate to the cloned directory**  
    Change your current directory to the cloned repository:
```
cd multiple_bebops
```
3.  **Edit the shortpress_3.sh file to set the SSID, PW, and IP**
    
    -   Open the shortpress_3.sh file in a text editor of your choice.
    -   Set the following variables:
        -   SSID: NCRLab
        -   PW: JollyPiano625
        -   IP: 192.168.1.1XX
    -   Ensure the IP address is in the same range as the other Bebops. Refer to the **Autonomy Park NCR Lab IP Reservations** document on Google Drive for the correct IP ranges. Once finished you will also need to add the new IP to the list.

## Step 2: Connect to the Bebop using Android Debug Bridge (adb)

1.  **Install adb**  
    If not already installed, install the Android Debug Bridge tools by running:
```
sudo apt-get install android-tools-adb
```
2.  **Connect adb to the Bebop**  
 Use a USB cable to connect the Bebop to your computer, press the power button on the back of the Bebop and wait for the light to remain solid. You now need to click the button 4 times and you should hear some beeping indication. Then run the following command to establish a connection:

```
adb connect 192.168.43.1:9050
```
   Upon successful connection, the CLI should display a message saying "connected to 192.168.43.1:9050".
   

## Step 3: Run Script and add to boot

1.  **Run the copy_files.sh script**  
    From the root of the cloned directory run the script:
```
./copy_files.sh`
```
2.  **Open a Bebop shell using adb**  
```
adb shell
```
3.  **Navigate to the /etc/init.d directory and edit the rcS file**
```
nano /etc/init.d/rcS
```
4.  **Add the following line to the end of the file**  
    Append the following line to ensure the shortpress_3.sh script runs on boot:
```
./bin/onoffbutton/shortpress_3.sh
```
5. **Now disconnect adb, and unplug and restart the bebop**
```
adb disconnect
```
## Notes

-   Ensure all IP addresses assigned to Bebops are unique and within the correct range as specified in the IP reservations document.
-   If you encounter issues with adb, verify that the Bebop is powered on and properly connected via USB.
- If you have any issues with read/write privelages run this command. It should already be called when you run the copy_files script.
```
adb shell mount -o remount,rw /
```
