from datetime import datetime, timedelta
import logging

from .apps.pdu.models import *
from .apps.env.models import *
from pyModbusTCP.client import ModbusClient
from django.db import transaction
from .apps.app import dbUtil

logger = logging.getLogger(__name__)


def storePduData():
    c = ModbusClient(host="10.0.0.54", port=502, unit_id=1, auto_open=True)
    # 0번 주소는 1~8 output들의 총합. 1~8은 그대로 output에 해당. 총 9개 데이터에서 읽는다.
    # upper, lower로 2바이트씩 분할된 값은 2배인 총 18개 데이터.
    currents = c.read_input_registers(100, 9)
    powers = c.read_input_registers(200, 9)
    energyCounters = c.read_input_registers(300, 18)
    tpfs = c.read_input_registers(400, 9)
    phaseShifts = c.read_input_registers(500, 9)
    reverseEnergyCounters = c.read_input_registers(600, 18)

    with transaction.atomic():
        for i in range(9):
            spd = StoredPduData(outputNum=i,
                                current=currents[i],
                                power=powers[i],
                                energyCounter=(energyCounters[2 *
                                                              i] << 16) & energyCounters[2*i+1],
                                tpf=tpfs[i],
                                phaseShift=phaseShifts[i],
                                reverseEnergyCounter=(reverseEnergyCounters[2*i] << 16) & reverseEnergyCounters[2*i+1])

            spd.save()
    logger.info('storePduData')


def deleteOldRecord():
    dbUtil.deleteRecordWithDateRange(
        StoredPduData, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Temperature, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Humidity, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Co2, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Light, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Camera, None, datetime.today()-timedelta(days=30))
    dbUtil.deleteRecordWithDateRange(
        Motor, None, datetime.today()-timedelta(days=30))
    logger.info('deleteOldRecord')


def test():
    logger.info('test')
    print("testprint")
