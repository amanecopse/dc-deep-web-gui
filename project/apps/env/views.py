from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json
import logging
from project.apps.env.models.power import Pdu
from project.apps.env.models.sensor import Sensor
from project.apps.env.serializers import *
from .models.dataCenter import Rack, Server
from project.apps.env.forms import *

REQUEST_DATA_KEY_FORM_NAME = "formName"
REQUEST_DATA_KEY_MODE = "mode"

REQUEST_DATA_VALUE_RACK_FORM = "RackForm"
REQUEST_DATA_VALUE_PDU_FORM = "PduForm"
REQUEST_DATA_VALUE_SENSOR_FORM = "SensorForm"
REQUEST_DATA_VALUE_SERVER_FORM = "ServerForm"

REQUEST_DATA_VALUE_MODE_SUBMIT_ADD = "formSubmitAdd"
REQUEST_DATA_VALUE_MODE_SUBMIT_DELETE = "formSubmitDelete"
REQUEST_DATA_VALUE_MODE_SUBMIT_EDIT = "formSubmitEdit"

REQUEST_DATA_VALUE_MODE_SHOW_ADD = "showModal"

MODEL_FIELD_RACK = "rack"
MODEL_FIELD_PDU = "pdu"
MODEL_FIELD_SENSOR = "sensor"
MODEL_FIELD_SERVER = "server"
MODEL_FIELD_RACK_NUM = "rackNum"
MODEL_FIELD_PDU_NUM = "pduNum"
MODEL_FIELD_SENSOR_NUM = "sensorNum"
MODEL_FIELD_SERVER_NUM = "serverNum"

logger = logging.getLogger(__name__)


class EnvView(View):

    def get(self, request):
        data = {'rackForm': RackForm(), 'pduForm': PduForm(), 'serverForm': ServerForm(), 'sensorForm': SensorForm(),
                'listData': getRackListData()}
        if request.is_ajax():  # Modal에서 보일 폼 구성을 반환한다

            requestMode = request.GET.get(REQUEST_DATA_KEY_MODE)
            form = None
            # Add 요청인 경우
            if requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_ADD:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)

                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    form = RackForm()
                elif formName == REQUEST_DATA_VALUE_PDU_FORM:
                    form = PduForm()
                elif formName == REQUEST_DATA_VALUE_SENSOR_FORM:
                    form = SensorForm()
                elif formName == REQUEST_DATA_VALUE_SERVER_FORM:
                    form = ServerForm()
                else:  # 알 수 없는 폼
                    return
            # Edit 요청인 경우
            elif requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_EDIT:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)

                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    rackNum = request.GET.get(MODEL_FIELD_RACK_NUM)
                    form = RackForm(instance=Rack.objects.get(rackNum=rackNum))
                elif formName == REQUEST_DATA_VALUE_PDU_FORM:
                    rackNum = request.GET.get(
                        MODEL_FIELD_RACK).get(MODEL_FIELD_RACK_NUM)
                    rack = Rack.objects.get(rackNum=rackNum)
                    pduNum = request.GET.get(MODEL_FIELD_PDU_NUM)
                    form = PduForm(instance=Pdu.objects.get(
                        rack=rack, pduNum=pduNum))
                elif formName == REQUEST_DATA_VALUE_SENSOR_FORM:
                    rackNum = request.GET.get(
                        MODEL_FIELD_RACK).get(MODEL_FIELD_RACK_NUM)
                    rack = Rack.objects.get(rackNum=rackNum)
                    sensorNum = request.GET.get(MODEL_FIELD_SENSOR_NUM)
                    form = SensorForm(
                        instance=Sensor.objects.get(rack=rack, sensorNum=sensorNum))
                elif formName == REQUEST_DATA_VALUE_SERVER_FORM:
                    rackNum = request.GET.get(
                        MODEL_FIELD_RACK).get(MODEL_FIELD_RACK_NUM)
                    rack = Rack.objects.get(rackNum=rackNum)
                    serverNum = request.GET.get(MODEL_FIELD_SERVER_NUM)
                    form = ServerForm(
                        instance=Server.objects.get(rack=rack, serverNum=serverNum))

                else:  # 알 수 없는 폼
                    return
            else:  # 알 수 없는 ajax 요청
                return

            return JsonResponse({'form': str(form)}, safe=False)
        return render(request, 'env/index.html', data)

    def post(self, request):
        data = {}
        if request.is_ajax():
            requestMode = request.GET.get(REQUEST_DATA_KEY_MODE)

            # Add 요청인 경우
            if requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_ADD:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)
                form = None

                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    form = RackForm(request.POST)
                elif formName == REQUEST_DATA_VALUE_PDU_FORM:
                    form = PduForm(request.POST)
                elif formName == REQUEST_DATA_VALUE_SENSOR_FORM:
                    form = SensorForm(request.POST)
                elif formName == REQUEST_DATA_VALUE_SERVER_FORM:
                    form = ServerForm(request.POST)
                else:  # 알 수 없는 폼
                    return

                if (form == None) or not form.is_valid:
                    return
                form.save()
            # Edit 요청인 경우
            elif requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_EDIT:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)

                # Rack form
                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    rackNum = request.POST.get(MODEL_FIELD_RACK_NUM)
                    form = RackForm(
                        request.POST, instance=Rack.objects.get(rackNum=rackNum))
                    if not form.is_valid:
                        return
                    form.save()

                else:  # 알 수 없는 폼
                    return

            # Delete 요청인 경우
            elif requestMode == REQUEST_DATA_VALUE_MODE_SUBMIT_DELETE:
                formName = request.GET.get(REQUEST_DATA_KEY_FORM_NAME)

                # Rack form
                if formName == REQUEST_DATA_VALUE_RACK_FORM:
                    rackNum = request.POST.get(MODEL_FIELD_RACK_NUM)
                    rack = Rack.objects.get(rackNum=rackNum)
                    rack.delete()
                else:  # 알 수 없는 폼
                    return
            else:  # 알 수 없는 ajax 요청
                return

            # ajax 응답 데이터
            data = json.loads(getRackListData())
            return JsonResponse({'rackForm': str(RackForm()), 'pduForm': str(PduForm()),
                                 'serverForm': str(ServerForm()), 'sensorForm': str(SensorForm()),
                                 'listData': data}, safe=False)
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
                {"id": 1, "rack": {~}, "pdu1": {~}, "pdu2": {~}, "pdu1Output": 3, "pdu2Output": 4, "serverNum": 1, "info": "test server1"},
                ~~~,
                ~~~
            ],
        }
    ]
    '''
    return json.dumps(listData)
