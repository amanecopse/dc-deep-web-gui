from django.shortcuts import render
from django.views import View
import logging
from project.apps.app.dbUtil import getLastNData
from project.apps.env.models.power import Pdu, PduData

from project.apps.env.models.sensor import Sensor, SensorData

logger = logging.getLogger(__name__)


class IndexView(View):

    def get(self, request):
        sensors = Sensor.objects.all()
        temperatureDatas = []
        humidityDatas = []
        for sensor in sensors:
            recentData = getLastNData(SensorData, 1, sensor=sensor)
            if (recentData == None) or (len(recentData) == 0):
                continue
            recentData = recentData[0]
            temperatureDatas.append(recentData.temperature)
            humidityDatas.append(recentData.humidity)
        pdus = Pdu.objects.all()
        pduDatas = []
        for pdu in pdus:
            recentData = getLastNData(PduData, 1, pdu=pdu, outputNum=0)
            if (recentData == None) or (len(recentData) == 0):
                continue
            recentData = recentData[0]
            pduDatas.append(recentData.power)

        data = {
            'temperaturePercent': int(sum(temperatureDatas)/len(temperatureDatas)),
            'humidityPercent': int(sum(humidityDatas)/len(humidityDatas)),
            'powerPercent': int(sum(pduDatas)/(len(pduDatas)*5000) * 100),
            'power': int(sum(pduDatas)),
            'powerTotal': len(pduDatas)*5000,
        }
        return render(request, 'app/index.html', data)

    def post(self, request):
        data = {}
        return render(request, 'app/index.html', data)
