import sys
import os
sys.path.insert(0, os.getcwd())
import dialogflow_v2 as dialogflow
from random import randint, seed, shuffle
import requests
import instaquiz
from aylienapiclient import textapi
import zulip
from typing import Any, Dict
import spellchecker
import mathbot
import codeforces
import wolframbot


zulip_client = zulip.Client(config_file="~/zuliprc")

client = textapi.Client("976cfa13", "b05f5525c81dd2a6551388ef411e1e52")


seed()


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


class TyroHandler(object):
    def usage(self) -> str:
        return '''tyro: the AI Bot'''

    def handle_message(self, message: Dict[str, Any], bot_handler: Any) -> None:
        msg = message['content'].strip()[:250]
        recv = msg.split()

        ## Hard-coded *********
        if recv[0] == 'site-gist':
            recv = recv[1:]
            if len(recv) == 0:
                url = "http://techcrunch.com/2015/04/06/john-oliver-just-changed-the-surveillance-reform-debate"
            else:
                url = recv[0]
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
            return
        
        if recv[0] == 'sentiment':
            recv = recv[1:]
            sentiment = client.Sentiment(
                {'text': 'John is a very good football player!'})
            bot_handler.send_reply(message, str(sentiment))
            return
        
        if recv[0] == "spellcheck":
            sentence = ""
            for words in recv[1:]:
                sentence += (words+' ')
            bot_handler.send_reply(
                message, spellchecker.check_spellings(sentence))
            return
        
        if recv[0] == "contests":
            bot_handler.send_reply(message, codeforces.get_contest_list())
            return

        if recv[0] == "evaluate":
            bot_handler.send_reply(
                message, mathbot.evaluate_all_expression(recv))
            return

        if recv[0] == "tellme":
            sentence = ""
            for words in recv[1:]:
                sentence += (words+' ')
            bot_handler.send_reply(
                message, wolframbot.get_short_answer(sentence))
            return

        ## end of hard-coded *********

        storage = bot_handler.storage
        cur_cmd = ''
        if storage.contains('cur_cmd'):
            cur_cmd = storage.get('cur_cmd')

        ## if exit irrespective of cur_cmd ****
        response = detect_intent_texts(
            'zulip-bot', 'unique', msg, 'en')
        if response is not None:
            intent = response.intent.display_name
            print('here')
            if intent == 'exit':
                print('there')
                bot_handler.send_reply(message, response.fulfillment_text)
                cur_cmd = ''
                storage.put('cur_cmd', cur_cmd)
                return

        ## if cur_cmd is set *************
        if cur_cmd == 'explain':
            ''' given a paragraph gets concepts then summarizes the contents of 
            the links returned in concepts '''
            if msg == '':
                text = "Apple was founded by Steve Jobs, Steve Wozniak and Ronald Wayne."
            else:
                text = msg
            concepts = client.Concepts({"text": text})
            output = ''
            cnt = 1
            for uri, value in concepts['concepts'].items():
                sfs = map(lambda c: c['string'], value['surfaceForms'])
                output += str(str(cnt) + ') **' +
                              ', '.join(sfs) + '** ' + uri + '\n')
                summary = client.Summarize({'url': uri, 'sentences_number': 2})
                for sentence in summary['sentences']:
                    output += str(sentence)
                output += '\n'
                cnt += 1
            bot_handler.send_reply(message, output)
            return
        elif cur_cmd == 'instaquiz':
            instaquiz.choose(recv, message, bot_handler)
            return

        ## cur_cmd is not set ***************

        if response is None:
            bot_handler.send_reply(
                message, 'I am sorry but I couldn\'t get that!')
            return
        intent = response.intent.display_name
        if intent == 'exit':
            bot_handler.send_reply(message, response.fulfillment_text)
            return
        elif intent == 'explain':
            cur_cmd = 'explain'
            bot_handler.send_reply(message, 'specify text to explain:')
            storage.put('cur_cmd', cur_cmd)
            return
        elif intent == 'instaquiz':
            cur_cmd = 'instaquiz'
            storage.put('cur_cmd', cur_cmd)
            instaquiz.choose(recv, message, bot_handler)
            return
        else:
            bot_handler.send_reply(message, response.fulfillment_text)
            return


handler_class = TyroHandler
