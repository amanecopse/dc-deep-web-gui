from django.shortcuts import render, HttpResponse
from django.db import models
from pyModbusTCP.client import ModbusClient
import logging

from app.models import StoredPduData, getDataFromNDaysAgo, MAX_OUTPUT_NUMBER, pduUnits


def index(request):
    logger = logging.getLogger(__name__)
    logger.info("index page")
    print("index page")
    c = ModbusClient(host="10.0.0.54", port=502, unit_id=1, auto_open=True)

    if request.method == "POST":
        keys = request.POST.keys()
        params = [[101, 0], [102, 0], [103, 0], [104, 0],
                  [105, 0], [106, 0], [107, 0], [108, 0]]
        if "o1_check" in keys:
            params[0][1] = 1
        if "o2_check" in keys:
            params[1][1] = 1
        if "o3_check" in keys:
            params[2][1] = 1
        if "o4_check" in keys:
            params[3][1] = 1
        if "o5_check" in keys:
            params[4][1] = 1
        if "o6_check" in keys:
            params[5][1] = 1
        if "o7_check" in keys:
            params[6][1] = 1
        if "o8_check" in keys:
            params[7][1] = 1
        for i in range(MAX_OUTPUT_NUMBER):
            c.write_single_register(params[i][0], params[i][1])

    outputs = c.read_holding_registers(101, MAX_OUTPUT_NUMBER)
    freq_volt = c.read_input_registers(0, 2)
    for i in range(8):
        if outputs[i] == 1:
            outputs[i] = "checked"
        else:
            outputs[i] = ""

    xVal, yVals = processPlotData('tpf')
    data = {'freqeuncy': round(freq_volt[0]/100),
            'voltage': round(freq_volt[1]/10),
            'o1': outputs[0], 'o2': outputs[1], 'o3': outputs[2], 'o4': outputs[3],
            'o5': outputs[4], 'o6': outputs[5], 'o7': outputs[6], 'o8': outputs[7],
            'xVal': xVal, 'yVals': yVals, }

    return render(request, 'app/index.html', data)


def processPlotData(fieldName):
    querySet = getDataFromNDaysAgo(StoredPduData, 10)

    xVal = querySet.filter(outputNum=0).values_list('dateTime')
    if xVal != None:
        xVal = list(map(
            lambda x: f'{{"year": {x[0].year}, "month": {x[0].month}, "month": {x[0].month}, "day": {x[0].day}, "hour": {x[0].hour}, "minute": {x[0].minute}}}', xVal))
    xVal = f"[{','.join(xVal)}]"

    yVals = []
    for i in range(MAX_OUTPUT_NUMBER+1):
        yVal = querySet.filter(outputNum=i).values_list(fieldName)
        if yVal != None:
            yVal = list(map(lambda x: float(x[0]), yVal))
        yVals.append(yVal)
    return xVal, yVals
