from datetime import datetime, timedelta
from django.db import models


def resetModel(model: models.Model):
    model.objects.all().delete()


def getDataFromNDaysAgo(model: models.Model, nDays) -> models.QuerySet:
    return model.objects.filter(dateTime__gte=datetime.today() -
                                timedelta(days=nDays))


def getLastNData(model: models.Model, n):
    arr = list(model.objects.order_by('-id')[:n])
    arr.reverse()
    return arr


class StoredPduData(models.Model):
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
