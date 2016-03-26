# Raspberry Spy #

Turn your Raspberry Pi into a way to take pictures at given intervals

### What is this repository for? ###

* Raspberry Spy helps you take pictures throughout the day and upload them to Google Drive

### How do I get set up? ###
Equipment:

* [Raspberry Pi models 1, 2 or 3](https://www.raspberrypi.org/products/)

* [Raspberry Pi power supply](https://www.raspberrypi.org/products/universal-power-supply/)

* [Raspberry Pi camera](https://www.raspberrypi.org/products/camera-module/)

* [Raspberry Pi wifi dongle](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=sr_1_1?s=electronics&ie=UTF8&qid=1458780799&sr=1-1&keywords=raspberry+pi+wireless)


### HTTP Methods ###

|HTTP   |Method                                                      |URI Action              |
|:-----:|:----------------------------------------------------------:|:----------------------:|
|GET    |http://[hostname]/raspberry-spy/api/v1.0/actions            |Retrieve list of actions|
|GET    |http://[hostname]/raspberry-spy/api/v1.0/actions/[action_id]|Retrieve an action      |
|POST   |http://[hostname]/raspberry-spy/api/v1.0/actions            |Create an action        |
|PUT    |http://[hostname]/raspberry-spy/api/v1.0/actions/[action_id]|Update an action        |
|DELETE |http://[hostname]/raspberry-spy/api/v1.0/actions/[action_id]|Stop an action          |
|UPDATE |http://[hostname]/raspberry-spy/api/v1.0/actions/[action_id]|Update an action        |
