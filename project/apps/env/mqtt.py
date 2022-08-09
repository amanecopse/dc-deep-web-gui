import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe("/cordy/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("gogogo.kr", 1883, 60)
