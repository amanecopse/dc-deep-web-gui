from django.db import models

# message type values: Temperature Humidity Co2 Light Camera Motor
SENSOR_TYPE_TEMPERATURE = 'temperature'
SENSOR_TYPE_HUMIDITY = 'humidity'
# SENSOR_TYPE_CO2 = 'co2'
# SENSOR_TYPE_LIGHT = 'light'
# SENSOR_TYPE_CAMERA = 'camera'
# SENSOR_TYPE_MOTOR = 'motor'

# keys: type mac celsius rh ppm lux index status
MSG_KEY_TYPE = 'type'
MSG_KEY_RACK_NUM = 'type'
MSG_KEY_PDU_NUM = 'type'
MSG_KEY_OUTPUT_NUM = 'type'
MSG_KEY_MAC = 'mac'
MSG_KEY_CELSIUS = 'celsius'
MSG_KEY_RH = 'rh'
MSG_KEY_PPM = 'ppm'
MSG_KEY_LUX = 'lux'
MSG_KEY_INDEX = 'index'
MSG_KEY_STATUS = 'status'


def insertRecordWithJsonDict(jsonDict):
    msgType = jsonDict[MSG_KEY_TYPE]
    msgMac = jsonDict[MSG_KEY_MAC]

    sensor = Sensor.objects.filter(mac=msgMac, sensorType=msgType)
    if len(sensor) != 1:  # 맥주소와 센서 종류에 일치하는 것이 db에 등록되어 있어야한다.
        print('not registered')
        return
    sensor = sensor[0]
    rackNum = sensor.rackNum
    pduNum = sensor.pduNum
    outputNum = sensor.outputNum

    if msgType == SENSOR_TYPE_TEMPERATURE:
        tmpr = TemperatureData(
            rackNum=rackNum,
            pduNum=pduNum,
            outputNum=outputNum,
            mac=jsonDict[MSG_KEY_MAC],
            celsius=jsonDict[MSG_KEY_CELSIUS])
        tmpr.save()
    elif msgType == SENSOR_TYPE_HUMIDITY:
        hmdt = HumidityData(
            rackNum=rackNum,
            pduNum=pduNum,
            outputNum=outputNum,
            mac=jsonDict[MSG_KEY_MAC],
            rh=jsonDict[MSG_KEY_RH])
        hmdt.save()
    # elif msgType == SENSOR_TYPE_CO2:
    #     co2 = Co2Data(
    #         rackNum=rackNum,
    #         pduNum=pduNum,
    #         outputNum=outputNum,
    #         mac=jsonDict[MSG_KEY_MAC],
    #         ppm=jsonDict[MSG_KEY_PPM])
    #     co2.save()
    # elif msgType == SENSOR_TYPE_LIGHT:
    #     light = LightData(
    #         rackNum=rackNum,
    #         pduNum=pduNum,
    #         outputNum=outputNum,
    #         mac=jsonDict[MSG_KEY_MAC],
    #         lux=jsonDict[MSG_KEY_LUX])
    #     light.save()
    # elif msgType == SENSOR_TYPE_CAMERA:
    #     camera = CameraData(
    #         rackNum=rackNum,
    #         pduNum=pduNum,
    #         outputNum=outputNum,
    #         mac=jsonDict[MSG_KEY_MAC],
    #         index=jsonDict[MSG_KEY_INDEX],
    #         status=jsonDict[MSG_KEY_STATUS])
    #     camera.save()
    # elif msgType == SENSOR_TYPE_MOTOR:
    #     motor = MotorData(
    #         rackNum=rackNum,
    #         pduNum=pduNum,
    #         outputNum=outputNum,
    #         mac=jsonDict[MSG_KEY_MAC],
    #         status=jsonDict[MSG_KEY_STATUS])
    #     motor.save()


class Sensor(models.Model):

    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputNum = models.IntegerField()
    mac = models.CharField(max_length=20)
    sensorType = models.CharField(max_length=20)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, type:{self.sensorType}'


class TemperatureData(models.Model):

    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputNum = models.IntegerField()
    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    celsius = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, celsius: {self.celsius}'


class HumidityData(models.Model):

    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputNum = models.IntegerField()
    mac = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now_add=True)
    rh = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, rh: {self.rh}'


# class Co2Data(models.Model):

#     rackNum = models.IntegerField()
#     pduNum = models.IntegerField()
#     outputNum = models.IntegerField()
#     mac = models.CharField(max_length=20)
#     dateTime = models.DateTimeField(auto_now_add=True)
#     ppm = models.DecimalField(max_digits=6, decimal_places=2)

#     def __str__(self):
#         return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, ppm: {self.ppm}'


# class LightData(models.Model):

#     rackNum = models.IntegerField()
#     pduNum = models.IntegerField()
#     outputNum = models.IntegerField()
#     mac = models.CharField(max_length=20)
#     dateTime = models.DateTimeField(auto_now_add=True)
#     lux = models.DecimalField(max_digits=6, decimal_places=2)

#     def __str__(self):
#         return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, lux: {self.lux}'


# class CameraData(models.Model):

#     rackNum = models.IntegerField()
#     pduNum = models.IntegerField()
#     outputNum = models.IntegerField()
#     mac = models.CharField(max_length=20)
#     dateTime = models.DateTimeField(auto_now_add=True)
#     index = models.CharField(max_length=20)
#     status = models.IntegerField()

#     def __str__(self):
#         return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, index: {self.index}, status: {self.status}'


# class MotorData(models.Model):

#     rackNum = models.IntegerField()
#     pduNum = models.IntegerField()
#     outputNum = models.IntegerField()
#     mac = models.CharField(max_length=20)
#     dateTime = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField()

#     def __str__(self):
#         return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, mac: {self.mac}, date:{self.dateTime}, status: {self.status}'
