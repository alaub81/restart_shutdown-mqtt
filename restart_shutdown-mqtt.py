#!/usr/bin/python3
import os, systemd.daemon, time
import paho.mqtt.client as mqtt, ssl

### set the variables
# MQTT Config
broker = "FQDN / IP ADDRESS"
port = 8883
publish_topic="home/attic/office"
clientid = "client-power"
hostname = "clientname"
username = "mosquitto"
password = "password"
insecure = True
qos = 1
retain_message = True
# Retry to connect to mqtt broker
mqttretry = 5

### do the stuff
print('Starting up Restart & Shutdown MQTT Service ...')

# just give some used variables an initial value
powerswitch = "Null"

### Functions
def publish(topic, payload):
  client.publish(publish_topic + "/" + topic,payload,qos,retain_message)

def on_connect(client, userdata, flags, rc):
  print("MQTT Connection established, Returned code=",rc)
  client.subscribe(publish_topic + "/" + hostname + "/system_power_switch", qos)

def on_message(client, userdata, message):
  global powerswitch
  if "system_power_switch" in message.topic:
    #print("MQTT system power payload:", str(message.payload.decode("utf-8")))
    powerswitch = str(message.payload.decode("utf-8"))

#MQTT Connection
mqttattempts = 0
while mqttattempts < mqttretry:
  try:
    client=mqtt.Client(clientid)
    client.username_pw_set(username, password)
    client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
    client.tls_insecure_set(insecure)
    client.connect(broker, port)
    client.loop_start()
    mqttattempts = mqttretry
  except :
    print("Could not establish MQTT Connection! Try again " + str(mqttretry - mqttattempts) + "x times")
    mqttattempts += 1
    if mqttattempts == mqttretry:
      print("Could not connect to MQTT Broker! exit...")
      exit (0)
    time.sleep(5)

# MQTT Subscription
client.on_message = on_message
client.on_connect = on_connect

# Tell systemd that our service is ready
systemd.daemon.notify('READY=1')

# finaly the loop
while True:
  try:
    #print("powerswitch Loop wert: ", powerswitch)
    if powerswitch == "shutdown":
      publish(hostname + "/system_power_switch", "on")
      print("System Shutdown")
      os.system('halt')
    elif powerswitch == "reboot":
      publish(hostname + "/system_power_switch", "on")
      print("System Reboot")
      os.system('reboot')
    time.sleep(1)

  except KeyboardInterrupt:
    print("Goodbye!")
    # At least close MQTT Connection
    client.disconnect()
    client.loop_stop()
    exit (0)

  except :
    print("An Error accured ... ")
    time.sleep(3)
    continue

# At least close MQTT Connection
client.disconnect()
client.loop_stop()

