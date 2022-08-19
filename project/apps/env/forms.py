from django import forms

from project.apps.env.models.dataCenter import *
from project.apps.env.models.power import Pdu
from project.apps.env.models.sensor import Sensor


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = '__all__'


class PduForm(forms.ModelForm):
    class Meta:
        model = Pdu
        fields = '__all__'


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__'


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
