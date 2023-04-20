                                                            # Data-Collector-RPI3
                                                            
### Necessary configuration to be set on the RPI before starting to use it
- Issue the command ifconfig on cmd to get the IP address of the RPI
- To SSH into the RPI enable the SSH config: Preferences -> Raspberry Pi Configuration -> Interfaces -> SSH: enable
- To setup camera module in RPI: 1) Refer to installation instruction from https://elinux.org/RPi-Cam-Web-Interface to setup the camera. 2) To check if Camera is working fine, browse the IPAddress of the server. 3) To be able to use the camera in python script disable the http option by a) sudo nano /etc/rc.local b) o	remove #START RASPIMJPEG SECTION c) restart RPI.
