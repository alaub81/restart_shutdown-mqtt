# restart_shutdown-mqtt
This Python script restarts or shuts down a Linux system via MQTT Publish. The whole thing is ideal in combination with the Raspberry Pi, an openHAB installation and a touch display. In my scenario I can either restart the underlying or another Linux system via HABPanel or even turn it off completely. HABPanel sends the "reboot" or "shutdown" command via an openHAB item to the MQTT broker. The topic there is subscribed in a Python script that runs as a system daemon and then executes a reboot or halt accordingly.
# Requirements
* Linux System
* Python3 Installation
* Python3 Paho MQTT Library
* MQTT Broker
* Optional: openHAB Installation
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

# Editieren der Dateien
nano /etc/systemd/system/restart_shutdown.service
nano /usr/local/sbin/restart_shutdown-mqtt.py
# Aktivieren des Autostart
systemctl enable restart_shutdown.service
systemctl start restart_shutdown.service

# Testing
Check if the service is runnig:
```bash
systemctl status restart_shutdown.service
```
Send 'reboot' or 'shutdown' via MQTT publish to your choiced topic.

# Whole Documentation of that Project:
More Informations here (Sorry, it's german, but just use your browsers transaltion tool): [Python_MQTT_System_Restart_und_Shutdown_Script](https://www.laub-home.de/wiki/Python_MQTT_System_Restart_und_Shutdown_Script)

# Questions, Help, Feedback
If you have any questions, you need help, or just have feedback for my first project here, just let me know!
