# restart_shutdown-mqtt
This Python script restarts or shuts down a Linux system via MQTT Publish. The whole thing is ideal in combination with the Raspberry Pi, an openHAB installation and a touch display. In my scenario I can either restart the underlying or another Linux system via HABPanel or even turn it off completely. HABPanel sends the "reboot" or "shutdown" command via an openHAB item to the MQTT broker. The topic there is subscribed in a Python script that runs as a system daemon and then executes a reboot or halt accordingly.
# Requirements
* Linux System
* Python3 Installation
* Python3 Paho MQTT Library
* MQTT Broker
* Optional: openHAB Installation

For Debian based Operating Systems:
```bash
apt install -y python3 python3-paho-mqtt
```
# Installation
```bash
cd /usr/src
git clone https://github.com/alaub81/restart_shutdown-mqtt.git
cp restart_shutdown-mqtt/restart_shutdown-mqtt.py /usr/local/sbin/
cp restart_shutdown-mqtt/restart_shutdown.service /etc/systemd/system/
chmod +x /usr/local/sbin/restart_shutdown-mqtt.py
```
# Configuration
Now you have to configure the MQTT connection in the `/usr/local/sbin/restart_shutdown-mqtt.py` script:
```python3
# MQTT Config
broker = "FQDN / IP ADDRESS" # --> Broker FQDN or IP address
port = 8883 # --> MQTT Broker TCP Port (8883 for the TLS Port, 1883 for the standard Port)
publish_topic="home/attic/office" # --> in which topic you want to publish
clientid = "client-dp" # --> MQTT Client ID, should be unique.
hostname = "clientname" # --> In this topic the helping MQTT values are published (lux goes directly into the topic)
username = "mosquitto" # --> MQTT username, if authentication is used
password = "password" # --> MQTT password, if authentication is used
insecure = True # --> if using a self signed certificate
qos = 1 # --> MQTT QoS level (0, 1, 2) 
retain_message = True # --> publish as a retained mqtt message (True, False)
```
And you have to edit the `/etc/systemd/system/display.service` if you are using the MQTT Broker in a Docker Container running on the same system
```bash
...
# Only needed if MQTT Broker is running in a Docker Container on the same Host
After=docker.service
After=docker.socket
```
you can use `nano` for editing:
```bash
nano /etc/systemd/system/restart_shutdown.service
nano /usr/local/sbin/restart_shutdown-mqtt.py
```
now you could also enable and start the systemd service
```bash
systemd daemon-reload
systemctl enable display.service
systemctl start display.service
```
# Testing
Check if the service is runnig:
```bash
systemctl status restart_shutdown.service
```
Send 'reboot' or 'shutdown' via MQTT publish to your choiced topic.

# Whole Documentation of that Project:
More Informations here (Sorry, it's german, but just use your browsers transaltion tool): [Python MQTT System Restart und Shutdown Script](https://www.laub-home.de/wiki/Python_MQTT_System_Restart_und_Shutdown_Script)

# Questions, Help, Feedback
If you have any questions, you need help, or just have feedback for my first project here, just let me know!
