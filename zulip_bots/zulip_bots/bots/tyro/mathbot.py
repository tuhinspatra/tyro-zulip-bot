import sys
import os
sys.path.insert(0, os.getcwd())

import requests
import json
from typing import Dict, Any

# class mathHandler(object):
#     def usage(self):
#         return '''
#             Get your mathematics expressions evaluated quickly :)
#         '''


def evaluate_all_expression(data):
    if data[1] == "evaluate":
        expressions = data[2:]
        query = {"expr": expressions, "precision": 10}
        endpoint = "http://api.mathjs.org/v4/"
        response = requests.post(endpoint, data=json.dumps(query))
        # print(response.json())
        answers = response.json()
        if answers['error'] != None:
            # bot_handler.send_reply(message,answers['error'])
            return answers['error']
        else:
            ret = ""
            for ans in answers['result']:
                ret = ret+ans+'\n\n'
            return ret
            # bot_handler.send_reply(message,ret)
# handler_class = mathHandler
