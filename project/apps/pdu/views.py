from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.db import models
from django.views import View
from pyModbusTCP.client import ModbusClient
import logging
import json
from project.apps.env.models.dataCenter import Rack
from project.apps.env.models.power import Pdu, PduData
from .pduUtil import pduUtil
from project.apps.app.dbUtil import getDataFromNDaysAgo, getLastNData

logger = logging.getLogger(__name__)


class PduView(View):

    REQUEST_TYPE_CHART_RENDER = 'chart render'
    REQUEST_TYPE_TABLE_RENDER = 'table render'
    REQUEST_TYPE_SWITCH_SETTING = 'switch setting'

    def get(self, request, rackNum, pduNum):
        rack = get_object_or_404(Rack, rackNum=rackNum)
        pdu = get_object_or_404(Pdu, rack=rack, pduNum=pduNum)
        if request.is_ajax():
            logger.info('ajax request with GET method')
            requestType = request.GET.get('type', 0)
            if requestType == PduView.REQUEST_TYPE_CHART_RENDER:
                fieldName = request.GET.get('fieldName', 0)
                xVal, yVals = processPlotData(fieldName)
                chartData = {'xVal': xVal, 'yVals': yVals, }
                return JsonResponse(chartData, safe=False)
            elif requestType == PduView.REQUEST_TYPE_TABLE_RENDER:
                tableData = list(map(
                    lambda x: [x.power, x.energyCounter, x.current], getLastNData(PduData, 9)))
                return JsonResponse(tableData, safe=False)

        modbusClient = ModbusClient(
            host=pdu.ip, port=502, unit_id=1, auto_open=True)

        if modbusClient.open():
            return self.renderPage(request, modbusClient, rackNum, pduNum, pdu)
        else:
            return HttpResponse(f'IP {pdu.ip} is not available')

    def post(self, request, rackNum, pduNum):
        rack = get_object_or_404(Rack, rackNum=rackNum)
        pdu = get_object_or_404(Pdu, rack=rack, pduNum=pduNum)
        modbusClient = ModbusClient(
            host=pdu.ip, port=502, unit_id=1, auto_open=True)

        if request.is_ajax():
            logger.info('ajax request with POST method')
            requestType = request.POST.get('type', 0)
            if requestType == PduView.REQUEST_TYPE_SWITCH_SETTING:
                switchIndex = request.POST.get('switchIndex', -1)
                switchState = request.POST.get('switchState', -1)

                if (switchIndex == -1) or (switchState == -1):
                    return

                modbusClient.write_single_register(
                    101+int(switchIndex), int(switchState))

                checks = modbusClient.read_holding_registers(
                    101, pduUtil.MAX_OUTPUT_NUMBER)
                return JsonResponse(checks, safe=False)

        return self.renderPage(request, modbusClient, rackNum, pduNum, pdu)

    def renderPage(self, request, modbusClient: ModbusClient, rackNum, pduNum, pdu):
        logger = logging.getLogger(__name__)
        logger.info("index page render")
        print("index page render")

        outputs = modbusClient.read_holding_registers(
            101, pduUtil.MAX_OUTPUT_NUMBER)
        freq_volt = modbusClient.read_input_registers(0, 2)

        xVal, yVals = processPlotData(pduUtil.PDU_VARIABLE_ENERGY_COUNTER, pdu)
        tableData = list(map(
            lambda x: [x.power, x.energyCounter, x.current], getLastNData(PduData, pduUtil.MAX_OUTPUT_NUMBER+1, pdu=pdu)))

        data = {'rackNum': rackNum,
                'pduNum': pduNum,
                'freqeuncy': round(freq_volt[0]/100),
                'voltage': round(freq_volt[1]/10),
                'outputCheck': outputs,
                'xVal': xVal, 'yVals': yVals, 'tableData': tableData}

        return render(request, 'pdu/index.html', data)


def processPlotData(fieldName, pdu):
    querySet = getDataFromNDaysAgo(PduData, 10, pdu=pdu)

    xVal = querySet.filter(outputNum=0).values_list('dateTime')
    if xVal != None:
        xVal = list(map(
            lambda x: f'{{"year": {x[0].year}, "month": {x[0].month}, "month": {x[0].month}, "day": {x[0].day}, "hour": {x[0].hour}, "minute": {x[0].minute}}}', xVal))
    xVal = json.loads(f"[{','.join(xVal)}]")
    yVals = []
    for i in range(pduUtil.MAX_OUTPUT_NUMBER+1):
        yVal = querySet.filter(outputNum=i).values_list(fieldName)
        if yVal != None:
            yVal = list(map(lambda x: float(x[0]), yVal))
        yVals.append(yVal)
    return xVal, yVals
