import hug
import os
import requests
import json
import re
from datetime import datetime
from botFunctions import URL, BOT_HEADERS,BOT_EMAIL,BOT_NAME
from botFunctions import bot_post_to_room, get_msg_sent_to_bot, process_bot_input_command


'''
Merchandise stock bot.  
Company knows where the trucks are at and how much inventory they have.
Simulate a db call with hard coded variables:
city/driver/contact/cases availalbe(DP,7UP,AWRB,KCUP)

bot command: <botname> <anything> --> help message
bot command: <botname> <city> --> show all drivers , all brands
bot command: <botname> <city> <brand> --> show drivers that have available inventory
'''


@hug.post('/bot', examples='bot')
def bot(body):
    """
        Test bot for new features.
    """
    print("GOT {}: {}".format(type(body), repr(body)))
    room_id = body["data"]["roomId"]
    identity = body["data"]["personEmail"]
    text = body["data"]["id"]
    print("see POST from {}".format(identity))
    if identity != BOT_EMAIL:
        print("{}-----{}".format(identity,BOT_EMAIL))
        command = get_msg_sent_to_bot(text, BOT_HEADERS)
        command = command.lower()
        command = (command.replace(BOT_NAME, '')).strip()
        command = (command.replace('@', '')).strip()
        #print("stripped command: {}".format(command))
        process_bot_input_command(room_id,command, BOT_HEADERS, BOT_NAME)
        #send_log_to_ss(BOT_NAME,str(datetime.now()),identity,command,room_id)


