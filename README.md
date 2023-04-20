                                                            # Data-Collector-RPI3
                                                            
This application is built to store observations from the sensor like temperature, humidity, thermal, brightness, and images into firebase as well as the local database tables.

---

### Necessary configuration to be set on the RPI before starting to use it
- Issue the command ifconfig on cmd to get the IP address of the RPI
- To SSH into the RPI enable the SSH config: Preferences -> Raspberry Pi Configuration -> Interfaces -> SSH: enable
- To setup camera module in RPI: 1) Refer to installation instruction from https://elinux.org/RPi-Cam-Web-Interface to setup the camera. 2) To check if Camera is working fine, browse the IPAddress of the server. 3) To be able to use the camera in python script disable the http option by a) sudo nano /etc/rc.local b) o	remove #START RASPIMJPEG SECTION c) restart RPI.

### Firebase and Local Database preparation
- Add the entry of the rpidescription in the Firebase Database -> RPI-details -> add new instance of the RPI and add field parameters with required information. Example: IPAddress: 172.21.197.141
         collection: blackbox
         location: growth room #1 (Middle)
         password: 12345
         type: rpi3
         username: sakshi-seth
- Create another entry of the RPI in the Firebase Database -> CollectionName(same as used in the above data)
- Create another entry of the RPI in the Storage to store images
- Create a database table in Data-Store.db on webserver for the respective RPI on webserver@128.192.158.63 path: /var/www/aspendb/probesearch/SensorsData
- Firebase account can be accessed using https://console.firebase.google.com/u/1/project/rpi-dataset/firestore/data/~2FRPI-details

---

### Flow of the application:

### Instructions
1. Clone this repository. \
`git clone https://github.com/sakshi-seth-17/Data-Collector-RPI3.git`

2. Make neccessary changes required in the app.py wrt specific RPI. \

3. Travel to the parent project directory and install the required python packages. \
`Create virtual environment – python3 -m venv venv` \
`source venv/bin/activate` \
`pip3 install -r requirement.txt` \
`To check if application is working fine run – python3 app.py` \

### Create service file to make the app run indefinitely
`sudo nano /lib/systemd/system/datacollector.service` \
Paste below lines inside the file by making necessary changes \
[Unit] \
Description=rpi0 \
After=multi-user.target \


[Service] \
WorkingDirectory=/home/sonya-cummings \
User=sonya-cummings \
Type=idle \
ExecStart=/home/sonya-cummings/DataCollector/venv/bin/python3 /home/sonya-cummings/DataCollector/app.py \
Restart=on-failure \
KillMode=process \
LimitMEMLOCK=infinity \
LimitNOFILE=65535 \
Type=simple \


[Install] \
WantedBy=multi-user.target \

`sudo chmod 644 /lib/systemd/system/datacollector.service` \
`sudo systemctl enable datacollector.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start datacollector.service` \
`sudo systemctl status datacollector.service` \
