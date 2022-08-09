from django.db import models


class Containment(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True)
    outputNum = models.IntegerField()
    current = models.DecimalField(max_digits=20, decimal_places=2)
    power = models.DecimalField(max_digits=20, decimal_places=2)
    energyCounter = models.DecimalField(max_digits=20, decimal_places=2)
    tpf = models.DecimalField(max_digits=20, decimal_places=2)
    phaseShift = models.DecimalField(max_digits=20, decimal_places=2)
    reverseEnergyCounter = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'output: {self.outputNum}, date:{self.dateTime}'
