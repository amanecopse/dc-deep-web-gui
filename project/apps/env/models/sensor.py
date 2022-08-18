from django.db import models

# message type values: Temperature Humidity Co2 Light Camera Motor
SENSOR_TYPE_TEMPERATURE = 'temperature'
SENSOR_TYPE_HUMIDITY = 'humidity'

# keys: type mac celsius rh ppm lux index status
MSG_KEY_TYPE = 'type'
MSG_KEY_MAC = 'mac'
MSG_KEY_CELSIUS = 'celsius'
MSG_KEY_RH = 'rh'
MSG_KEY_PPM = 'ppm'
MSG_KEY_LUX = 'lux'
MSG_KEY_INDEX = 'index'
MSG_KEY_STATUS = 'status'


def insertRecordWithJsonDict(jsonDict):
    msgType = jsonDict.get(MSG_KEY_TYPE, None)
    msgMac = jsonDict.get(MSG_KEY_MAC, None)

    if (msgType == None) or (msgMac == None):
        return

    sensor = Sensor.objects.filter(mac=msgMac)
    if len(sensor) != 1:  # 맥주소와 센서 종류에 일치하는 것이 db에 등록되어 있어야한다.
        print(__name__+': not registered sensor')
        return
    sensor = sensor[0]

    if msgType == SENSOR_TYPE_TEMPERATURE:
        sd = SensorData(
            rack=sensor.rack,
            pdu=sensor.pdu,
            sensor=sensor,
            dataType=msgType,
            dataUnit=MSG_KEY_CELSIUS,
            value=jsonDict[MSG_KEY_CELSIUS])
        sd.save()
    elif msgType == SENSOR_TYPE_HUMIDITY:
        sd = SensorData(
            rack=sensor.rack,
            pdu=sensor.pdu,
            sensor=sensor,
            dataType=msgType,
            dataUnit=MSG_KEY_RH,
            value=jsonDict[MSG_KEY_RH])
        sd.save()


class Sensor(models.Model):
    from project.apps.env.models.dataCenter import Rack
    from project.apps.env.models.power import Pdu

    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu = models.ForeignKey(Pdu, on_delete=models.CASCADE)
    pduOutput = models.IntegerField()
    sensorNum = models.IntegerField()
    mac = models.CharField(max_length=20)
    info = models.CharField(max_length=200)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, sensorNum: {self.sensorNum}, mac: {self.mac}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rack', 'sensorNum'], name='rack_sensor'),
        ]


class SensorData(models.Model):
    from project.apps.env.models.dataCenter import Rack
    from project.apps.env.models.power import Pdu
    dataTypeChoices = (
        (SENSOR_TYPE_TEMPERATURE, SENSOR_TYPE_TEMPERATURE),
        (SENSOR_TYPE_HUMIDITY, SENSOR_TYPE_HUMIDITY)
    )
    dataUnitChoices = (
        (MSG_KEY_CELSIUS, MSG_KEY_CELSIUS),
        (MSG_KEY_RH, MSG_KEY_RH)
    )

    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu = models.ForeignKey(Pdu, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)
    dataType = models.CharField(
        max_length=20, choices=dataTypeChoices, default=SENSOR_TYPE_TEMPERATURE)
    dataUnit = models.CharField(
        max_length=20, choices=dataUnitChoices, default=MSG_KEY_CELSIUS)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, sensorNum: {self.sensor.sensorNum},  date:{self.dateTime}, {self.dataUnit}: {self.value}'
