from django.db import models

MSG_KEY_TEMPERATURE = 'temperature'
MSG_KEY_HUMIDITY = 'humidity'
MSG_KEY_MAC = 'mac'


def insertRecordWithJsonDict(jsonDict):
    msgMac = jsonDict.get(MSG_KEY_MAC, None)
    msgTemperature = jsonDict.get(MSG_KEY_TEMPERATURE, None)
    msgHumidity = jsonDict.get(MSG_KEY_HUMIDITY, None)

    if (msgMac == None) or (msgTemperature == None) or (msgHumidity == None):
        return

    sensor = Sensor.objects.filter(mac=msgMac)
    if len(sensor) != 1:  # 맥주소와 센서 종류에 일치하는 것이 db에 등록되어 있어야한다.
        print(__name__+': not registered sensor')
        return
    sensor = sensor[0]

    sd = SensorData(
        rack=sensor.rack,
        pdu=sensor.pdu,
        sensor=sensor,
        temperature=jsonDict[MSG_KEY_TEMPERATURE],
        humidity=jsonDict[MSG_KEY_HUMIDITY])
    sd.save()


class Sensor(models.Model):
    from project.apps.env.models.dataCenter import Rack
    from project.apps.env.models.power import Pdu

    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu = models.ForeignKey(Pdu, on_delete=models.CASCADE)
    pduOutput = models.IntegerField()
    sensorNum = models.IntegerField()
    mac = models.CharField(max_length=20, unique=True)
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

    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu = models.ForeignKey(Pdu, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    humidity = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, sensorNum: {self.sensor.sensorNum},  date:{self.dateTime}, temperature: {self.temperature}, humidity: {self.humidity}'
