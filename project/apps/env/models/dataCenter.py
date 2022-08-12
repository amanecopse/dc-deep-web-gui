from django.db import models


class Rack(models.Model):
    rackNum = models.IntegerField(primary_key=True)
    info = models.CharField(max_length=200)

    def __str__(self):
        return f'rackNum: {self.rackNum}, info: {self.info}'


class Server(models.Model):
    from project.apps.env.models.power import Pdu
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    pdu1 = models.ForeignKey(
        Pdu, on_delete=models.CASCADE, related_name='pdu1')
    pdu2 = models.ForeignKey(
        Pdu, on_delete=models.CASCADE, related_name='pdu2')
    pdu1Output = models.IntegerField()
    pdu2Output = models.IntegerField()
    serverNum = models.IntegerField()
    info = models.CharField(max_length=200)

    def __str__(self):
        return f'rackNum: {self.rack.rackNum}, serverNum: {self.serverNum}, info: {self.info}'
