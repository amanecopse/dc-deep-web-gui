from datetime import datetime, timedelta
import logging

from project.apps.env.models.power import Pdu, PduData
from project.apps.env.models.sensor import *
from pyModbusTCP.client import ModbusClient
from django.db import transaction
from .apps.app import dbUtil

logger = logging.getLogger(__name__)


def storePduData():

    for pdu in Pdu.objects.all():
        pduIp = pdu.ip
        modbusClient = ModbusClient(
            host=pduIp, port=502, unit_id=1, auto_open=True)
        modbusClient.open()
        if not modbusClient.is_open:
            logger.info('can not connect with IP:'+pduIp)
            continue
        # 0번 주소는 1~8 output들의 총합. 1~8은 그대로 output에 해당. 총 9개 데이터에서 읽는다.
        # upper, lower로 2바이트씩 분할된 값은 2배인 총 18개 데이터.
        currents = modbusClient.read_input_registers(100, 9)
        powers = modbusClient.read_input_registers(200, 9)
        energyCounters = modbusClient.read_input_registers(300, 18)
        tpfs = modbusClient.read_input_registers(400, 9)
        phaseShifts = modbusClient.read_input_registers(500, 9)
        reverseEnergyCounters = modbusClient.read_input_registers(600, 18)

        with transaction.atomic():
            for i in range(pdu.outputCount + 1):
                pd = PduData(
                    rack=pdu.rack,
                    pdu=pdu,
                    outputNum=i,
                    current=currents[i],
                    power=powers[i],
                    energyCounter=(
                        energyCounters[2*i] << 16) & energyCounters[2*i+1],
                    tpf=tpfs[i],
                    phaseShift=phaseShifts[i],
                    reverseEnergyCounter=(reverseEnergyCounters[2*i] << 16) & reverseEnergyCounters[2*i+1])

                pd.save()
        modbusClient.close()
    logger.info('storePduData')


def deleteOldRecord():
    dbUtil.deleteRecordWithDateRange(
        PduData, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        SensorData, None, datetime.today()-timedelta(days=30))
    logger.info('deleteOldRecord')


def test():
    logger.info('test')
    print("testprint")
