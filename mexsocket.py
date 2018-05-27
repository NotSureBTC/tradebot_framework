#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 13:08:44 2018

@author: Kam Kardootsian
"""
from bitmex_websocket import BitMEXWebsocket
import config

if config.bitmex_test==False:
    ep="https://www.bitmex.com/api/v1"
else:
    ep="https://testnet.bitmex.com/api/v1"
ordersym = "XBTUSD"
ws = BitMEXWebsocket(endpoint=ep,symbol=ordersym, api_key=config.bitmex_auth['apiKey'], api_secret=config.bitmex_auth['secret'])


def get_wsbidasklast():
    ticker=ws.get_instrument()
    return(ticker['bidPrice'],ticker['askPrice'],ticker['lastPrice'])