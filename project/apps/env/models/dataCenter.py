from django.db import models


class DataCenter(models.Model):
    racks = models.CharField(max_length=200)

    def __str__(self):
        return f'racks: {self.racks}'


class Rack(models.Model):
    rackNum = models.IntegerField(primary_key=True)
    deviceCount = models.IntegerField()
    sensorCount = models.IntegerField()
    pduCount = models.IntegerField()

    def __str__(self):
        return f'rackNum: {self.rackNum}, deviceCount: {self.deviceCount}, sensorCount: {self.sensorCount}, pduCount: {self.pduCount}'


class Device(models.Model):
    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputNum = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, name: {self.name}'
