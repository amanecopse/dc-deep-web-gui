from django.db import models


class Pdu(models.Model):
    from project.apps.env.models.dataCenter import Rack
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pduNum = models.IntegerField()
    outputCount = models.IntegerField()
    ip = models.CharField(max_length=20)
    info = models.CharField(max_length=200)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, pduNum: {self.pduNum}, info: {self.info}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rack', 'pduNum'], name='rack_pdu'),
        ]


class PduData(models.Model):
    from project.apps.env.models.dataCenter import Rack
    dateTime = models.DateTimeField(auto_now_add=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu = models.ForeignKey(Pdu, on_delete=models.CASCADE)
    outputNum = models.IntegerField()
    current = models.DecimalField(max_digits=20, decimal_places=2)
    power = models.DecimalField(max_digits=20, decimal_places=2)
    energyCounter = models.DecimalField(max_digits=20, decimal_places=2)
    tpf = models.DecimalField(max_digits=20, decimal_places=2)
    phaseShift = models.DecimalField(max_digits=20, decimal_places=2)
    reverseEnergyCounter = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, pduNum: {self.pdu.pduNum}, output: {self.outputNum}, date: {self.dateTime}'
