# aqualogic
This version is intended to be used as a custom_components build within Home Assistant. These modifications repaired my intermittent switches although I cannot speak for other switches such as chlorinator or aux_2.

Copy the aqualogic directory and drop it straight into the custom_components directory within Home Assistant. It will override the default aqualogic integration. You can check the logs on restart to see if it recognizes aqualogic as a custom component.

-------

A python library to interface with Hayward/Goldline AquaLogic/ProLogic pool controllers. Based on Goldline prototol decoding work done by draythomp (http://www.desert-home.com/p/swimming-pool.html). Used by the [Home Assistant AquaLogic component](https://www.home-assistant.io/components/aqualogic/).

Since the Goldline protocol uses RS-485, a hardware interface is required. I'm using an [RS-485 to Ethernet adapter](https://www.usriot.com/products/rs485-to-ethernet-converter.html), though you could use some other type of adapter (e.g. RS-485 to RS-232); the library supports both socket and serial connections.

In addition to the API, the library also provides a rudimentary web interface. This allows the user to cycle through the menu system to perform manual tasks such as setting the heater temperature.

- [RS-485 Notes](https://github.com/swilson/aqualogic/wiki/RS%E2%80%90485-Notes)
- [TriStar VS Pump Notes](https://github.com/swilson/aqualogic/wiki/TriStar-VS-Pump-Notes)
- [Upgrading the AquaLogic Firmware](https://github.com/swilson/aqualogic/wiki/Upgrading-the-AquaLogic-Firmware)
- [Wired Remote Repair](https://github.com/swilson/aqualogic/wiki/Wired-Remote-Repair)

Tested on an AquaLogic P4 with Main Software Revision 2.91. YMMV.

This project is not affiliated with or endorsed by Hayward Industries Inc. in any way. 
