from django.contrib import admin
from project.apps.env.models.dataCenter import DataCenter, Device, Rack
from project.apps.env.models.power import *
from project.apps.env.models.sensor import *

admin.site.register([Sensor, TemperatureData, HumidityData,
                    Pdu, PduData, DataCenter, Rack, Device])
