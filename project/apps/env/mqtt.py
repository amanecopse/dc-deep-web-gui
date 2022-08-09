import json
import paho.mqtt.client as mqtt


# message type values: Temperature Humidity Co2 Light Camera Motor
MSG_TYPE_TEMPERATURE = 'temperature'
MSG_TYPE_HUMIDITY = 'humidity'
MSG_TYPE_CO2 = 'co2'
MSG_TYPE_LIGHT = 'light'
MSG_TYPE_CAMERA = 'camera'
MSG_TYPE_MOTOR = 'motor'

# keys: type mac celsius rh ppm lux index status
MSG_KEY_TYPE = 'type'
MSG_KEY_MAC = 'mac'
MSG_KEY_CELSIUS = 'celsius'
MSG_KEY_RH = 'rh'
MSG_KEY_PPM = 'ppm'
MSG_KEY_LUX = 'lux'
MSG_KEY_INDEX = 'index'
MSG_KEY_STATUS = 'status'


def on_connect(client, userdata, flags, rc):
    client.subscribe("/cordy/#")


def on_message(client, userdata, msg):
    from project.apps.env.models import Camera, Co2, Humidity, Light, Motor, Temperature
    print(msg.topic+" "+str(msg.payload))
    jsonDict = json.loads(msg.payload)
    msgType = jsonDict[MSG_KEY_TYPE]
    if msgType == MSG_TYPE_TEMPERATURE:
        tmpr = Temperature(
            mac=jsonDict[MSG_KEY_MAC], celsius=jsonDict[MSG_KEY_CELSIUS])
        tmpr.save()
    elif msgType == MSG_TYPE_HUMIDITY:
        hmdt = Humidity(mac=jsonDict[MSG_KEY_MAC],
                        rh=jsonDict[MSG_KEY_RH])
        hmdt.save()
    elif msgType == MSG_TYPE_CO2:
        co2 = Co2(mac=jsonDict[MSG_KEY_MAC],
                  ppm=jsonDict[MSG_KEY_PPM])
        co2.save()
    elif msgType == MSG_TYPE_LIGHT:
        light = Light(mac=jsonDict[MSG_KEY_MAC],
                      lux=jsonDict[MSG_KEY_LUX])
        light.save()
    elif msgType == MSG_TYPE_CAMERA:
        camera = Camera(mac=jsonDict[MSG_KEY_MAC],
                        index=jsonDict[MSG_KEY_INDEX],
                        status=jsonDict[MSG_KEY_STATUS])
        camera.save()
    elif msgType == MSG_TYPE_MOTOR:
        motor = Motor(mac=jsonDict[MSG_KEY_MAC],
                      status=jsonDict[MSG_KEY_STATUS])
        motor.save()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("gogogo.kr", 1883, 60)
