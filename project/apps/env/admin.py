from django.contrib import admin
from project.apps.env.models.dataCenter import *
from project.apps.env.models.power import *
from project.apps.env.models.sensor import *

admin.site.register([Sensor, SensorData,
                    Pdu, PduData, Rack, Server])
