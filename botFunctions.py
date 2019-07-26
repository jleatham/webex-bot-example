import os
import sys
import random
import requests
import json
import urllib.request
from requests_toolbelt.multipart.encoder import MultipartEncoder


BOT_EMAIL = os.environ['BOT_EMAIL']
BOT_NAME = os.environ['BOT_NAME']

EXAMPLE_STOCK_RESULT = [
        ["JL is in Dallas and has 3 cases of DRP", "example@example.com", "(555) 555-5555"],
        ["CG is in San Fransisco and has 5 cases of 7UP", "example@example.com", "(555) 555-5555"],
        ["GK is in Seattle and has 2 cases of KCUPs", "example@example.com", "(555) 555-5555"]
]

URL = "https://api.ciscospark.com/v1/messages"

BOT_HEADERS = {
    'Authorization': os.environ['BOT_TOKEN'],
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}


def bot_send_gif(room_id, gif, message):
    #try to post
    payload = {"roomId": room_id,
               "markdown": message,
               "files":[gif]}
    response = requests.request("POST", 'https://api.ciscospark.com/v1/messages', data=json.dumps(payload), headers=BOT_HEADERS)
    #error handling
    print(f"sending gif to {room_id}")
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")

def bot_send_gif_v2(room_id, message, url):
    #try to post
    urllib.request.urlretrieve(url, 'gif.gif')
    m = MultipartEncoder({
                      'roomId': room_id,
                      'text': message,
                      'files': ('gif.gif', open(gif, 'rb'),
                      'image/gif')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                    headers={'Authorization': os.environ['BOT_TOKEN'],
                    'Content-Type': m.content_type})
    return r.text




def get_msg_sent_to_bot(msg_id, headers):
    urltext = URL + "/" + msg_id
    payload = ""

    response = requests.request("GET", urltext, data=payload, headers=headers)
    response = json.loads(response.text)
    print(response)
    #print ("Message to bot : {}".format(response["text"]))
    return response["text"]



def process_bot_input_command(room_id,command, headers, bot_name):
    """ 
        Give generic response for now if spoken to.
        Add a test command to run what it would look like
    """
    test_command_list = ['test']
    pause_command_list = ['stop','pause']
    example_command_list = ['example']
    possible_command_list = test_command_list + pause_command_list + example_command_list

    command_list = command.split(' ')
    event_trigger = list(set(command_list).intersection(possible_command_list))
    print(event_trigger)
    if event_trigger:
        '''
        #remove command trigger and keep what is left
        for i in event_trigger:
            command = command.replace(i,'').strip()
        '''
        print("made it to event trigger")
        if any(item in test_command_list for item in event_trigger):
            print("made it to test")
            msg_list = []
            
            msg_list.append("Test response \n\n")
            msg_list.append("This is markup text: **Bold** \n\n")
            msg = ''.join(msg_list)
            response = bot_post_to_room(room_id, msg, headers)
        elif any(item in pause_command_list  for item in event_trigger):
            msg_list = []
            
            msg_list.append("**Just an example** \n\n")
            msg_list.append("blah \n\n")
            msg = ''.join(msg_list)
            response = bot_post_to_room(room_id, msg, headers)    
        elif any(item in example_command_list  for item in event_trigger):
            stock_query = [x for x in event_trigger if (x not in example_command_list)]
            process_stock_query(room_id,stock_query,headers)

    else:
        bot_post_to_room(room_id,"Only commands I know are: **TEST** , and **pause** .  All values hard-coded at the moment and messages sent on schedule.",headers)




def bot_post_to_room(room_id, message, headers):
    #try to post
    payload = {"roomId": room_id,"markdown": message}
    response = requests.request("POST", URL, data=json.dumps(payload), headers=headers)
    #error handling
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")

def process_stock_query(room_id,stock_query,headers):
    print(f"Stock Query = {stock_query}")
    if not stock_query:
        msg = random.choice(EXAMPLE_STOCK_RESULT)
    bot_post_to_room(room_id,msg,headers)
