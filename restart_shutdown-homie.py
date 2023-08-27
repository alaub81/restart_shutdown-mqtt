#!/usr/bin/python3
import os, systemd.daemon, time
import paho.mqtt.client as mqtt, ssl

### set the variables
# MQTT Config
broker = "FQDN / IP ADDRESS"
port = 8883
mqttclientid = "client-power-homie"
clientname="clientname Power"
clientid = "clientname-power"
nodes="power"
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
  client.publish("homie/" + clientid + "/" + topic,payload,qos,retain_message)

def on_connect(client, userdata, flags, rc):
  print("MQTT Connection established, Returned code=",rc)
  client.subscribe("homie/" + clientid + "/" + nodes + "/systempowerswitch/set", qos)
  # homie client config
  publish("$state","init")
  publish("$homie","4.0")
  publish("$name",clientname)
  publish("$nodes",nodes)
  # homie node config
  publish(nodes + "/$name","System Power")
  publish(nodes + "/$properties","systempowerswitch")
  publish(nodes + "/systempowerswitch", "on")
  publish(nodes + "/systempowerswitch/$name","System Power Switch")
  publish(nodes + "/systempowerswitch/$datatype","enum")
  publish(nodes + "/systempowerswitch/$format","shutdown,reboot")
  publish(nodes + "/systempowerswitch/$retained","true")
  publish(nodes + "/systempowerswitch/$settable","true")
  # homie stae ready
  publish("$state","ready")

def on_message(client, userdata, message):
  global powerswitch
  global powerstate
  if "systempowerswitch/set" in message.topic:
    #print("MQTT system power set payload:", str(message.payload.decode("utf-8")))
    powerswitch = str(message.payload.decode("utf-8"))

def on_disconnect(client, userdata, rc):
  print("MQTT Connection disconnected, Returned code=",rc)

#MQTT Connection
mqttattempts = 0
while mqttattempts < mqttretry:
  try:
    client=mqtt.Client(mqttclientid)
    client.username_pw_set(username, password)
    client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
    client.tls_insecure_set(insecure)
    client.will_set("homie/" + clientid + "/$state","lost",qos,retain_message)
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
client.on_disconnect = on_disconnect

# Tell systemd that our service is ready
systemd.daemon.notify('READY=1')

# finaly the loop
while True:
  try:
    #print("powerswitch Loop wert: ", powerswitch)
    if powerswitch == "shutdown":
      powerswitch = "Null"
      print("System Shutdown")
      publish("$state","disconnected")
      publish(nodes + "/systempowerswitch", "off")
      client.disconnect()
      client.loop_stop()
      os.system('halt')
    elif powerswitch == "reboot":
      powerswitch = "Null"
      print("System Reboot")
      publish("$state","disconnected")
      publish(nodes + "/systempowerswitch", "reboot")
      client.disconnect()
      client.loop_stop()
      os.system('reboot')
    time.sleep(1)

  except KeyboardInterrupt:
    print("Goodbye!")
    # At least close MQTT Connection
    publish("$state","disconnected")
    time.sleep(1)
    client.disconnect()
    client.loop_stop()
    exit (0)

  except :
    print("An Error accured ... ")
    time.sleep(3)
    continue

# At least close MQTT Connection
print("Script stopped")
publish("$state","disconnected")
time.sleep(1)
client.disconnect()
client.loop_stop()

