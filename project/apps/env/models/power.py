from django.db import models


class Pdu(models.Model):
    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputCount = models.IntegerField()
    ip = models.CharField(max_length=20)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, outputCount: {self.outputCount}, ip: {self.ip}'


class PduData(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    rackNum = models.IntegerField()
    pduNum = models.IntegerField()
    outputNum = models.IntegerField()
    ip = models.CharField(max_length=20)
    current = models.DecimalField(max_digits=20, decimal_places=2)
    power = models.DecimalField(max_digits=20, decimal_places=2)
    energyCounter = models.DecimalField(max_digits=20, decimal_places=2)
    tpf = models.DecimalField(max_digits=20, decimal_places=2)
    phaseShift = models.DecimalField(max_digits=20, decimal_places=2)
    reverseEnergyCounter = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rackNum}, pduNum: {self.pduNum}, output: {self.outputNum}, date: {self.dateTime}'
