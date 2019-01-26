from random import randint, seed, shuffle
from typing import Any, Dict
import requests

from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='5ddc332a7d3a4683aec7f28731d5dd86')
model = app.public_models.general_model
seed()
ans = -1
auth_token = ''

def start_game(message: Dict[str, Any], bot_handler: Any) -> None:
    '''used by instagram picture quiz'''
    global auth_token
    global ans
    r = requests.get(
        'https://api.instagram.com/v1/users/self/media/recent/?access_token=' + auth_token).json()
    r = r['data']
    shuffle(r)
    num = min(len(r)-1, 4)
    if ans != -1:
        ans = (ans ^ randint(0, num) ^ 1) % num
    else:
        ans = randint(0, num)
    response = model.predict_by_url(
        r[ans]['images']['standard_resolution']['url'])
    response = response['outputs'][0]['data']['concepts'][:5]
    shuffle(response)
    reply = 'Which of the following images represents "' + \
        str(response[0]['name']) + '" and "' + \
        str(response[1]['name']) + '" ?'
    bot_handler.send_reply(message, reply)
    reply = ''
    for i in range(num+1):
        reply = '[' + str(i + 1) + ')](' + str(r[i]['images']
                                                ['low_resolution']['url']) + ')'
        bot_handler.send_reply(message, reply)

def choose(recv, message, bot_handler):
    global auth_token
    global ans
    help_str = ''' show 5 images from instagram to user and asks
     which image should be tagged two given words '''
    if bot_handler.storage.contains('instaquiz_ans'):
        ans = int(bot_handler.storage.get('instaquiz_ans'))
    if bot_handler.storage.contains('instaquiz_auth'):
        auth_token = bot_handler.storage.get('instaquiz_auth')
    if len(recv) > 0 and recv[0] == 'answer' and ans != -1:
        if ans == int(recv[1]) - 1:
            bot_handler.send_reply(message, 'Correct!')
        else:
            bot_handler.send_reply(
                message, 'Oops, AI says ' + str(ans + 1) + '!')
    elif auth_token != '':
        ''' we have access token of user, start the game'''
        start_game(message, bot_handler)
    elif len(recv) > 0 and recv[0] == 'code':
        data = {'client_id': '143ed8666d4d47a0a800ccb070a3899a',
                'client_secret': '491ccbd334fd4cb881937f7a458f4332',
                'grant_type': 'authorization_code',
                'redirect_uri': 'https://testbot.zulipchat.com',
                'code': recv[1]}
        r = requests.post(
            url='https://api.instagram.com/oauth/access_token', data=data)
        r = r.json()
        auth_token = r['access_token']
        start_game(message, bot_handler)
    else:
        auth_url = 'https://api.instagram.com/oauth/authorize/?client_id=143ed8666d4d47a0a800ccb070a3899a&redirect_uri=https://testbot.zulipchat.com&response_type=code'
        bot_handler.send_reply(
            message, '**click** to authorize: ' + auth_url)
        bot_handler.send_reply(
            message, 'reply with the code from url as:\n "code <code>"')
