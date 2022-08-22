from datetime import datetime, timedelta
from django.db import models


def resetModel(model: models.Model):
    model.objects.all().delete()


def deleteRecordWithDateRange(model: models.Model, dateFrom: datetime, dateTo: datetime):
    if dateFrom == None:
        model.objects.filter(dateTime__lte=dateTo).delete()
    else:
        model.objects.filter(dateTime__gte=dateFrom,
                             dateTime__lte=dateTo).delete()


def getDataFromNDaysAgo(model: models.Model, nDays, **kwargs) -> models.QuerySet:
    return model.objects.filter(dateTime__gte=datetime.today() -
                                timedelta(days=nDays), **kwargs)


def getLastNData(model: models.Model, n, **kwargs):
    arr = list(model.objects.filter(**kwargs).order_by('-id')[:n])
    arr.reverse()
    return arr
