import sys
import os
sys.path.insert(0, os.getcwd())

from typing import Any, Dict
import zulip
zulip_client = zulip.Client(config_file="~/zuliprc")

from aylienapiclient import textapi
client = textapi.Client("976cfa13", "b05f5525c81dd2a6551388ef411e1e52")


from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='5ddc332a7d3a4683aec7f28731d5dd86')
model = app.public_models.general_model

import requests
from random import randint, seed, shuffle
seed()

import dialogflow_v2 as dialogflow

def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response is None:
        return None
    return response.query_result


class HelloWorldHandler(object):
    _token = ''
    _ans = -1
    def usage(self) -> str:
        return '''tyro: the AI Bot'''

    def start_game(self, message: Dict[str, Any], bot_handler: Any) -> None:
        '''used by instagram picture quiz'''
        r = requests.get(
            'https://api.instagram.com/v1/users/self/media/recent/?access_token=' + self._token).json()
        r = r['data']
        shuffle(r)
        num = min(len(r)-1, 4)
        if self._ans != -1: self._ans = (self._ans ^ randint(0, num) ^ 1) % num
        else: self._ans = randint(0, num)    
        response = model.predict_by_url(r[self._ans]['images']['standard_resolution']['url'])
        response = response['outputs'][0]['data']['concepts'][:5]
        shuffle(response)
        reply = 'Which of the following images represents "' + \
            str(response[0]['name']) + '" and "' + str(response[1]['name']) + '" ?'
        bot_handler.send_reply(message, reply)
        reply = ''
        for i in range(num+1):
            reply = '[' + str(i + 1) + ')](' + str(r[i]['images']
                                     ['low_resolution']['url']) + ')'
            bot_handler.send_reply(message, reply)

            
        # response = model.predict_by_url(r['data'][1]['images']['low_resolution']['url'])
        # bot_handler.send_reply(message, response['outputs'][0]['data']['concepts'][1]['name'])

        

    def handle_message(self, message: Dict[str, Any], bot_handler: Any) -> None:
        # if the particular idea can be implemented using intents and entities
        storage = bot_handler.storage
        cur_cmd = ''
        msg = message['content'].strip()
        response = detect_intent_texts(
            'zulip-bot', 'unique', msg, 'en')
        if response.intent.display_name == 'exit':
            bot_handler.send_reply(message, response.fulfillment_text)
            return
        if storage.contains('cur_cmd'):
            cur_cmd = storage.get('cur_cmd')
        recv = msg.split()
        if cur_cmd == '':
            response = detect_intent_texts(
                'zulip-bot', 'unique', msg, 'en')
            if response is None:
                bot_handler.send_reply(
                    message, 'I am sorry but I couldn\'t get that!')
                return
            intent = response.intent.display_name
            if intent == 'explain':
                cur_cmd = 'explain'
                bot_handler.send_reply(message, 'specify text to explain:')
                storage.put('cur_cmd', cur_cmd)
                return
            elif intent == 'exit':
                bot_handler.send_reply(message, 'Sure!')
                cur_cmd = ''
                storage.put('cur_cmd', cur_cmd)
                return
            else:
                bot_handler.send_reply(message, response.fulfillment_text)
                return


        if cur_cmd == 'explain':
            ''' given a paragraph gets concepts then summarizes the contents of 
            the links returned in concepts '''
            if msg == '':
                text = "Apple was founded by Steve Jobs, Steve Wozniak and Ronald Wayne."
            else: text = msg
            concepts = client.Concepts({"text": text})
            output = ''
            cnt = 1
            for uri, value in concepts['concepts'].items():
                sfs = map(lambda c: c['string'], value['surfaceForms'])
                output += str(str(cnt) + ') **' + ', '.join(sfs) + '** ' + uri + '\n')
                summary = client.Summarize({'url': uri, 'sentences_number': 2})
                for sentence in summary['sentences']:
                    output += str(sentence)
                output += '\n'
                cnt += 1
            bot_handler.send_reply(message, output)
            return
        elif recv[0] == 'site-gist':
            recv = recv[1:] 
            if len(recv) == 0:
                url = "http://techcrunch.com/2015/04/06/john-oliver-just-changed-the-surveillance-reform-debate"
            else: url = recv[0]
            if not url.startswith('h'):
                url = 'http://' + url
            extract = client.Extract({"url": url, "best_image": True})
            output = ''
            if extract['author'] != '':
                output += 'by ' + extract['author'] + '\n'
            if extract['image'] != '':
                output += extract['image'] + '\n'
            
            summary = client.Summarize({'url': url, 'sentences_number': 3})
            for sentence in summary['sentences']:
                    output += str(sentence)
            if output == '':
                output = 'The site has no data to summarize.\n'
            bot_handler.send_reply(message, output)
        elif recv[0] == 'sentiment':
            recv = recv[1:]
            sentiment = client.Sentiment(
                {'text': 'John is a very good football player!'})
            bot_handler.send_reply(message, str(sentiment))

        elif recv[0] == 'instaquiz':
            help_str = ''' show 5 images from instagram to user and ask which image should be tagged two given words '''
            
            recv = recv[1:]
            if len(recv) > 0 and recv[0] == 'answer' and self._ans != -1:
                if self._ans == int(recv[1]) - 1:
                    bot_handler.send_reply(message, 'Correct!')
                else:
                    bot_handler.send_reply(message, 'Oops, AI says ' + str(self._ans + 1) + '!')
            elif self._token != '':
                ''' we have access token of user, start the game'''
                self.start_game(message, bot_handler)
            elif len(recv) > 0 and recv[0] == 'code':
                data = {'client_id': '143ed8666d4d47a0a800ccb070a3899a',
                        'client_secret': '491ccbd334fd4cb881937f7a458f4332',
                        'grant_type': 'authorization_code',
                        'redirect_uri': 'https://testbot.zulipchat.com',
                        'code': recv[1]}
                r = requests.post(url='https://api.instagram.com/oauth/access_token', data=data)
                r = r.json()
                self._token = r['access_token']
                self.start_game(message, bot_handler)   
            else:
                auth_url = 'https://api.instagram.com/oauth/authorize/?client_id=143ed8666d4d47a0a800ccb070a3899a&redirect_uri=https://testbot.zulipchat.com&response_type=code'
                bot_handler.send_reply(message, '**click** to authorize: ' + auth_url)
                bot_handler.send_reply(message, 'reply with the code from url as:\n "code <code>"')
            # response = model.predict_by_url('https://samples.clarifai.com/metro-north.jpg')
            # bot_handler.send_reply(message, str(response))
        else:
            bot_handler.send_reply(message, detect_intent_texts('zulip-bot', 'unique', ' '.join(recv), 'en'))
        

        

handler_class = HelloWorldHandler
