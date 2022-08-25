from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from project.apps.app.dbUtil import getDataFromNDaysAgo

from project.apps.env.models.dataCenter import Rack
from project.apps.env.models.sensor import Sensor, SensorData
import json


class SensorView(View):

    REQUEST_TYPE_CHART_RENDER = 'chart render'

    def get(self, request, rackNum, sensorNum):
        rack = get_object_or_404(Rack, rackNum=rackNum)
        sensor = get_object_or_404(Sensor, rack=rack, sensorNum=sensorNum)

        if request.is_ajax():
            requestType = request.GET.get('type', None)
            if requestType == SensorView.REQUEST_TYPE_CHART_RENDER:
                fieldName = request.GET.get('fieldName', None)
                xVal, yVals = processChartData(fieldName, sensor)
                chartData = {'xVal': xVal, 'yVals': [yVals], }
                return JsonResponse(chartData, safe=False)

        temperatureXVal, temperatureYVal = processChartData(
            'temperature', sensor)
        humidityXVal, humidityYVal = processChartData(
            'humidity', sensor)
        data = {'temperature': {'xVal': temperatureXVal, 'yVal': temperatureYVal},
                'humidity': {'xVal': humidityXVal, 'yVal': humidityYVal},
                'rackNum': rackNum, 'sensorNum': sensorNum,
                }
        return render(request, 'sensor/index.html', data)

    def post(self, request, rackNum, sensorNum):
        return


def processChartData(fieldName, sensor: Sensor):
    querySet = getDataFromNDaysAgo(SensorData, 10, sensor=sensor)

    xVal = querySet.values_list('dateTime')
    if xVal != None:
        xVal = list(map(
            lambda x: f'{{"year": {x[0].year}, "month": {x[0].month}, "month": {x[0].month}, "day": {x[0].day}, "hour": {x[0].hour}, "minute": {x[0].minute}}}', xVal))
    xVal = json.loads(f"[{','.join(xVal)}]")
    yVal = querySet.values_list(fieldName)
    if yVal != None:
        yVal = list(map(lambda x: float(x[0]), yVal))
    return xVal, yVal
