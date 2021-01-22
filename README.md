# Webcam-EyeTracker
 Webcam based pupil-cr eye tracker
## Overview
 This repository is a small project to implement an eye-tracking system at low cost. It may provide a more affordable solution for those who need high speed eye tracking.
## Requirements
* A webcam
    * Remove IR-cut (infrared filter). It is a tiny blue glass covering the sensor or the lens. Note that for most of the webcam, this remove process is **IRREVERSIBLE**. Also, if you find it hard to focus the camera correctly after removing the IR cut, you can **replace** the IR cut with a piece of quartz glass. (With the same size and thickness)
    * Support high frame rate (200 fps or higher is recommended)
* An infrared lightsource
    * Our device shows that an 1 watt infrared LED is enough.
* A PC with Windows OS
    * We bought a webcam which uses `DirectShow` API to operate, therefore we must choose a specific operating system.
    * However, since we used `OpenCV` to fetch images, it is highly possible to run this program in Unix-like system by making few changes.
    * We think Raspberry Pi is capable of supporting the whole system. And it would be helpful to compile your own `NumPy` and `OpenCV` with SIMD support, if the speed is your first priority.
## Test Device
## Usage