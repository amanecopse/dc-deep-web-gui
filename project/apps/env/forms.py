from django import forms

from project.apps.env.models.dataCenter import Rack


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['rackNum', 'info']
