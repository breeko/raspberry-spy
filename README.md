# Raspberry Spy #

Turn your Raspberry Pi into a way to take pictures at given intervals

### What is this repository for? ###

* Raspberry Spy helps you take pictures throughout the day and upload them to Google Drive

### How do I get set up? ###
Equipment:
* [Raspberry Pi models 1, 2 or 3](https://www.raspberrypi.org/products/)

* [Raspberry Pi power supply](https://www.raspberrypi.org/products/universal-power-supply/)

* [Raspberry Pi camera](https://www.raspberrypi.org/products/camera-module/)

* Optional: [Raspberry Pi wifi dongle](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=sr_1_1?s=electronics&ie=UTF8&qid=1458780799&sr=1-1&keywords=raspberry+pi+wireless)


Setup:
* [Setup Raspberry Pi](https://www.raspberrypi.org/help/noobs-setup/)

* [Install camera](https://www.raspberrypi.org/help/camera-module-setup/)

* Optional: [Google Drive account](https://www.google.com/drive/)

* Download repo

* Run python camera.py to snap picture saved to folder called 'images'


Optional arguments:

*  -f Folder to store pictures

*  -m Frequency in minutes of pictures

*  -t Time during which camera will be activated every day (e.g. 10:00-21:00)

*  -u Whether to upload to Google Drive