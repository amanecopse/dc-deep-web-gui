import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if client == MqttClient.getClient():
        client.subscribe("/cordy/#")


def on_message(client, userdata, msg):
    from .models.sensor import insertRecordWithJsonDict

    try:
        print(msg.topic+" "+str(msg.payload), client)
        insertRecordWithJsonDict(json.loads(msg.payload))
    except:
        print(__name__+': decoding error')


class MqttClient():
    client = None

    @classmethod
    def getClient(cls):
        if cls.client == None:
            cls.client = mqtt.Client()
            cls.client.on_connect = on_connect
            cls.client.on_message = on_message
            cls.client.connect("gogogo.kr", 1883, 60)
        return cls.client
