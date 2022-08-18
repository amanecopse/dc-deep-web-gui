from rest_framework import serializers
from .models.dataCenter import *
from .models.power import *
from .models.sensor import *


class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = '__all__'


class PduSerializer(serializers.ModelSerializer):

    rack = RackSerializer()

    class Meta:
        model = Pdu
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):

    rack = RackSerializer()
    pdu = PduSerializer()

    class Meta:
        model = Sensor
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):

    rack = RackSerializer()
    pdu1 = PduSerializer()
    pdu2 = PduSerializer()

    class Meta:
        model = Server
        fields = '__all__'
