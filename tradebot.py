#!/usr/bin/env python2
# coding=utf-8
from __future__ import print_function
import time
import logging
#logging.basicConfig(level=logging.INFO)
import mexorders
from indicators import *
from notifications import send_sms
from utilities import *
import ExchgData

import config

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
dh = logging.FileHandler('full.log')
dh.setLevel(logging.DEBUG)
ih = logging.FileHandler('tradebot.log')
ih.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
ffm = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
cfm = logging.Formatter('[%(asctime)s] %(message)s')
sh.setFormatter(cfm)
dh.setFormatter(ffm)
ih.setFormatter(ffm)

log.addHandler(sh)
log.addHandler(dh)
log.addHandler(ih)
log.info("Logger initialized")

tl = logging.getLogger('trades')
tl.setLevel(logging.DEBUG)
tfh = logging.FileHandler('trades.log')
tsh = logging.StreamHandler()
tfh.setLevel(logging.DEBUG)
tsh.setLevel(logging.INFO)
tff = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
tsf = logging.Formatter('[%(asctime)s] %(message)s')
tfh.setFormatter(tff)
tsh.setFormatter(tsf)
tl.addHandler(tfh)
tl.addHandler(tsh)
tl.info("Trade Logger Initialized")

def report_trade(action, ordersize, stacked, price):
	report_string="action: %s\tordersize: %d\tstacked: %d\tprice: %.2f" % (action, ordersize, stacked, price)
	tl.info(report_string)
	log.debug(report_string)
	send_sms(report_string)


def m15hist_positive(exchgdata):
	# m15 for the div detection
	(t, o, h, l, c, v) = exchgdata.get_split_tohlcv('15m', 34)
	exchgdata.dprint_last_candles('15m', 5)
	(m15kvo, m15signal) = klinger_kama(h, l, c, v)
	m15hist = m15kvo[-1] - m15signal[-1]
	log.info("m15hist is %.2f" % m15hist)	
	positive = True
	if m15hist <= 0:
		positive = False
	return positive

sleeptime = 30

send_sms('Trading Bot Active!')		

# main loop
bfxdata = ExchgData.ExchgData('bfx')

last_hist_positive = m15hist_positive(bfxdata)
hist_positive = last_hist_positive

while [ 1 ]:
	log.debug("Main loop")
	mexorders.update_bracket_pct(config.sl, config.tp)

	hist_positive = m15hist_positive(bfxdata)

	shorts = mexorders.get_position_size('short')
	longs = mexorders.get_position_size('long')
	(bid, ask, last) = mexorders.get_bidasklast()
	# if h3 kvo has flipped, flip positions
	if hist_positive and not last_hist_positive:
		mexorders.cancel_open_orders()
		time.sleep(1)
		mexorders.smart_order('Buy', shorts+config.ordersize)
		report_trade("GOING LONG", shorts+config.ordersize, longs+config.ordersize, last)
	elif not hist_positive and last_hist_positive:
		mexorders.cancel_open_orders()
		time.sleep(1)
		mexorders.smart_order('Sell', longs+config.ordersize)
		report_trade("GOING SHORT", longs+config.ordersize, shorts+config.ordersize, last)

	last_hist_positive = hist_positive

	# now print some status info
	mexorders.print_positions()
	mexorders.print_open_orders()
	totalbal = mexorders.get_balance_total()
	freebal = mexorders.get_balance_free()
	log.info("Total Balance: %.4f, Free Balance: %.4f" % (totalbal, freebal))
	log.info( "Loop completed, sleeping for %d seconds" % sleeptime)
	time.sleep(sleeptime)

