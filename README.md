# Webcam-EyeTracker
 Webcam based pupil-cr eye tracker
## Overview
 This repository is a small project to implement an eye-tracking system at low cost. It may provide a more affordable solution for those who need high speed eye tracking.
## Requirements
* A webcam
    * Remove IR-cut (infrared filter). It is a tiny blue glass covering the sensor or the lens. Note that for most of the webcam, this remove process is **IRREVERSIBLE**. Also, if you find it hard to focus the camera correctly after removing the IR cut, you can **replace** the IR cut with a piece of quartz glass. (With the same size and thickness)
    * Support high frame rate (200 fps or higher is recommended)
* An infrared lightsource
    * Our configuration shows that an 1 watt infrared LED is enough.
* A PC with Windows OS
    * We bought a webcam which uses `DirectShow` API to operate, therefore we must choose a specific operating system.
    * However, since we used `OpenCV` to fetch images, it is highly possible to run this program in Unix-like system by making few changes.
    * We think Raspberry Pi is capable of supporting the whole system. And it would be helpful to compile your own `NumPy` and `OpenCV` with SIMD support, if the speed is your first priority.
## Performance
 This program is written and tested on a laptop with Intel Core i5-7300HQ CPU. The tracking refresh rate (dry run without actual video input) can achieve around 450 Hz.  
 Please note that the data recording and data streaming functions is executed by `QTimer` with time interval of 1ms, thus the data reporting rate (200~300 Hz in our own tests) is limited. Moreover, the data presented by these two function may not be synchronized. These problems may be addressed in the near future.
 ## Usage
 ### Configure Hardware
 ### Select ROI
  Click the Select ROI button on main window, drag the mouse to choose ROI. Press **Enter** to confirm your selection.  
  Since the Select ROI window is a built-in function in `OpenCV`, you need to close this window manually, and reopen it if you want to reselect your region of intrest.
 ### Choose a Proper Threshold
 ### Calibrate the Tracking System
 ### Validate the Calibration
 ### Start Tracking and Collecting Data
 ### Stop and Exit