from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
import logging
from project.apps.env.models.power import Pdu
from project.apps.env.models.sensor import Sensor
from project.apps.env.serializers import *
from .models.dataCenter import Rack, Server
from project.apps.env.forms import RackForm

REQUEST_DATA_KEY_FORM_NAME = "formName"
REQUEST_DATA_KEY_MODE = "mode"
REQUEST_DATA_VALUE_RACK_FORM = "RackForm"
REQUEST_DATA_VALUE_MODE_SUBMIT_ADD = "formSubmitAdd"
REQUEST_DATA_VALUE_MODE_SUBMIT_DELETE = "formSubmitDelete"
REQUEST_DATA_VALUE_MODE_SUBMIT_EDIT = "formSubmitEdit"

RACK_FIELD_RACK_NUM = "rackNum"
PDU_FIELD_PDU_NUM = "pduNum"
SENSOR_FIELD_SENSOR_NUM = "sensorNum"
SERVER_FIELD_SERVER_NUM = "serverNum"

logger = logging.getLogger(__name__)


class EnvView(View):

    def get(self, request):
        data = {'form': RackForm(), 'listData': getRackListData()}
        return render(request, 'env/index.html', data)

    def post(self, request):
        data = {}
        if request.is_ajax():
            requestMode = request.GET.get(REQUEST_DATA_KEY_MODE)
            if requestMode == None:
                return
            # Add 요청 폼인 경우
            if requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_ADD:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)
                if formName == None:
                    return
                # Rack form
                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    form = RackForm(request.POST)
                    if form.is_valid:
                        form.save()
                        data = json.loads(getRackListData())
                        return JsonResponse({'listData': data}, safe=False)
            # Edit 요청 폼인 경우
            if requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_EDIT:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)
                if formName == None:
                    return
                # Rack form
                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    rackNum = request.POST.get(RACK_FIELD_RACK_NUM)
                    form = RackForm(
                        request.POST, instance=Rack.objects.get(rackNum=rackNum))
                    if form.is_valid:
                        form.save()
                        data = json.loads(getRackListData())
                        return JsonResponse({'listData': data}, safe=False)

            # Delete 요청 폼인 경우
            if requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_DELETE:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)
                if formName == None:
                    return
                # Rack form
                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    rackNum = request.POST.get(RACK_FIELD_RACK_NUM)
                    rack = Rack.objects.get(rackNum=rackNum)
                    rack.delete()
                    data = json.loads(getRackListData())
                    return JsonResponse({'listData': data}, safe=False)
            return
        return render(request, 'env/index.html', data)


def getRackListData():
    listData = []
    racks = Rack.objects.all()
    rackDicts = list(Rack.objects.all().values())
    for i in range(len(racks)):
        pduDicts = PduSerializer(
            Pdu.objects.filter(rack=racks[i]), many=True).data
        sensorDicts = SensorSerializer(
            Sensor.objects.filter(rack=racks[i]), many=True).data
        serverDicts = ServerSerializer(
            Server.objects.filter(rack=racks[i]), many=True).data
        # pduDicts = list(Pdu.objects.filter(rack=racks[i]).values())
        # sensorDicts = list(Sensor.objects.filter(rack=racks[i]).values())
        # serverDicts = list(Server.objects.filter(rack=racks[i]).values())
        listData.append({
            'rack': rackDicts[i],
            'pdus': pduDicts,
            'sensors': sensorDicts,
            'servers': serverDicts,
        })
    '''
    json 구조
    [
        {
            "rack": {"rackNum":1, "info":"~~~"},
            "pdus": [
                {"id": 1, "rack": {~}, "pduNum": 1, "outputCount": 8, "ip": "10.0.0.54", "info": "test pdu1"},
                ~~~,
                ~~~
            ],
            "sensors": [
                {"id": 1, "rack": {~}, "pdu": {~}, "pduOutput": 1, "sensorNum": 1, "mac": "dc:a6:32:ed:3e:6e", "info": "test sensor1"},
                ~~~,
                ~~~
            ],
            "servers": [
                {"id": 1, "rack": {~}, "pdu": {~}, "pdu2_id": 1, "pdu1Output": 3, "pdu2Output": 4, "serverNum": 1, "info": "test server1"},
                ~~~,
                ~~~
            ],
        }
    ]
    '''
    return json.dumps(listData)
