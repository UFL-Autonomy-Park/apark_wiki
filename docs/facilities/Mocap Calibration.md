# Motion Capture Camera Calibration

If a camera goes down or is replaced, the system must be recalibrated.

## Steps

1. **Remove all robots with markers from the camera field of view**  
   - Place the robots in a locker or cover them to avoid interference.

2. **Set the OptiTrack reference**
   - Obtain the **wand** and the **OptiTrack calibration square**.
   - Place the OptiTrack at the lab coordinate origin.
   - Align the square so its axes match the lab coordinate axes.
   ![coordinate](../facilities/Mocap%20Calibration/mocap_coodinate_system.png)

   ![wand](../facilities/Mocap%20Calibration/Wand.jpg)

   ![OptiTrack placement](../facilities/Mocap%20Calibration/OptiTrack.jpg)

3. **Start wanding**
   - Launch **Motive**.
   - Click **Start Wanding**.
   - Move the wand throughout the lab so that all cameras collect samples.

4. **Calculate calibration**
   - Continue wanding until each camera collects **several thousand samples**.
   - Click **Calculate**.

5. **Apply calibration**
   - Click **Apply Result**.
   - Save the **calibration file**.

6. **Set ground plane**
   - Click **Set Ground Plane** to finalize the coordinate frame.