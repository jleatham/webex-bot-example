import os
import sys
import random
import requests
import json
import urllib.request
from requests_toolbelt.multipart.encoder import MultipartEncoder


BOT_EMAIL = os.environ['BOT_EMAIL']
BOT_NAME = os.environ['BOT_NAME']

CITY_SAMPLE = ["San Francisco","Dallas","Seattle","Houston","San Jose","Brooklyn","Detroit","Reno","Las Vegas","Vancouver"]
NAME_SAMPLE = ["José Joaquín Moraga","Jed York","John Neely Bryan","Jerry Jones","Paul Allen","Luther Collins"]
INVENTORY_SAMPLE = ["dp","canada-dry","awrb","gingerale","crush"]

EXAMPLE_STOCK_RESULT = [
        ["JL is in Dallas and has 3 cases of DRP", "example@example.com", "(555) 555-5555"],
        ["CG is in San Fransisco and has 5 cases of 7UP", "example@example.com", "(555) 555-5555"],
        ["GK is in Seattle and has 2 cases of KCUPs", "example@example.com", "(555) 555-5555"]
]

NAME_SAMPLE_2 = [["José Joaquín Moraga","moraga@example.com","(111) 111-1111"],["Jed York","york@example.com","(222) 222-2222"],["John Neely Bryan","bryan@example.com","(333) 333-3333"],["Jerry Jones","jones@example.com","(444) 444-4444"],["Paul Allen","allen@example.com","(555) 555-5555"],["Luther Collins","collins@example.com","(666) 666-6666"]]

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
        Provides a few different command options based in different lists. (commands should be lower case)
        Combines all lists together and checks if any keyword commands are detected...basically a manually created case/switch statement
        For each possible command, do something
        Is there an easier way to do this?
    """
    test_command_list = ['test']
    pause_command_list = ['stop','pause']
    example_command_list = ['example']
    inventory_command_list = INVENTORY_SAMPLE
    possible_command_list = test_command_list + pause_command_list + example_command_list + inventory_command_list

    command_list = command.split(' ')
    event_trigger = list(set(command_list).intersection(possible_command_list))
    print(event_trigger)
    if event_trigger:
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
            stock_query = [x for x in command_list if (x not in example_command_list)]
            process_stock_query(room_id,stock_query,headers)
        elif any(item in inventory_command_list  for item in event_trigger):
            msg_list = []
            msg_list.append(f"We have you located in the city of **{random.choice(CITY_SAMPLE)}** \n\n")
            first_name = random.choice(NAME_SAMPLE_2)

            print(NAME_SAMPLE_2)
            print(first_name)
            temp_name_sample = NAME_SAMPLE_2.copy()
            temp_name_sample.remove(first_name)
            print(temp_name_sample)
            second_name = random.choice(temp_name_sample)
            print(second_name)
            msg_list.append(f"**{first_name[0]}** currently has **{random.randint(1,10)}** cases of {event_trigger[0].upper()} and is {random.randint(1,10)} miles away\n\n")
            msg_list.append(f"**{second_name[0]}** currently has **{random.randint(1,10)}** cases of {event_trigger[0].upper()} and is {random.randint(1,10)} miles away\n\n")
            msg_list.append(f"Contact info: {first_name[1]}    {first_name[2]}  \n\n")
            msg_list.append(f"Contact info: {second_name[1]}    {second_name[2]}  \n\n")
            msg = ''.join(msg_list) 
            bot_post_to_room(room_id,msg,headers)
    else:
        msg_list = []
        '''
        msg_list.append("How to use bot: \n\n")
        msg_list.append("**example** {city}  --> don't include {city} if you want a random selection \n\n")
        msg_list.append("If you are in a room with multiple people, be sure to @ the bot \n\n")
        msg_list.append("@KDRP-stock-bot **example** dallas \n\n")
        '''
        msg_list.append(f"Just type in the product and I will find who has that inventory in your current city.  Current options: \n\n")
        msg_list.append(f"**{str(inventory_command_list).strip('[').strip(']')}** \n\n")
        msg = ''.join(msg_list)        
        bot_post_to_room(room_id,msg,headers)




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
        print(response)

def process_stock_query(room_id,stock_query,headers):
    print(f"Stock Query = {stock_query}")
    if not stock_query:
        msg = random.choice(EXAMPLE_STOCK_RESULT)
    elif "dallas" in stock_query:
        msg = EXAMPLE_STOCK_RESULT[0]         
    elif "san" in stock_query:
        msg = EXAMPLE_STOCK_RESULT[1]
    elif "seattle" in stock_query:
        msg = EXAMPLE_STOCK_RESULT[2]

    bot_post_to_room(room_id,msg[0],headers)
