# tradebot_framework
A framework for bitcoin trading bots

*AS OF RIGHT NOW ONLY BFX AND BITMEX FUNCTIONALITY IS IMPLEMENTED*

*USE AT YOUR OWN RISK*

Requirements:

 * Python 2
 * ccxt
 * twilio
 * requests
 * numpy
 * tulipy

# Sample Trade Bot

*THIS BOT IMPLEMENTS A SIMPLE M15 KVO / SIGNAL STRATEGY THAT WILL PROBABLY LOSE MONEY! USE AT YOUR OWN RISK*

To use the sample trade bot, copy config.py.example to config.py and put in your BitMEX credentials. If you use testnet credentials make sure to set the bitmex test setting to "True".

You should set stoplosses in the config file as a percentage and the bot will bracket your trade with a stop market / limit order stoplooss / take profit bracket, which will be updated based on entry price automatically.

Finally, you can add Twilio credentials to have the bot text you when it trades.

I recommend running the bot in screen like ./tradebot.py. It will output info to the console, and will log extensive debug information in full.log, and log trades in trades.log.
