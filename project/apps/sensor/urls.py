from django.urls import path

from project.apps.sensor.views import SensorView

app_name = 'sensor'

urlpatterns = [
    path('<int:rackNum>/<int:sensorNum>/', SensorView.as_view(), name='index'),
]
