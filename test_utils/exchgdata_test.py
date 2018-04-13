#!/usr/bin/env python2

from ExchgData import ExchgData
from time import sleep
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
fm = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
sh.setFormatter(fm)
log.addHandler(sh)

bfxdata = ExchgData('bfx')

log.debug("Starting...")
while [ True ]:
	#bfxdata.update_candles('5m')
	#print bfxdata.get_last_ts('5m')
	m5candles = bfxdata.get_candles('5m', 10)
	m15candles = bfxdata.get_candles('15m', 10)
	log.info("m5: %.2f, m15: %.2f" % (m5candles[-1][4], m15candles[-1][4]))
	sleep(30)
