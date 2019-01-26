import sys
import os
sys.path.insert(0, os.getcwd())

import requests,json
from typing import Dict,Any
import datetime

# class cfHandler(object):
#     def usage(self):
#         return '''
#             Get the future contests list on codeforces
#         '''
def get_contest_list(message:Dict[str,str],bot_handler:Any):
    print(message['content'])
    data=message['content'].split()
    if data[0]=='contest':
        if data[1]=='codeforces':
            endpoint='http://codeforces.com/api/contest.list'
            response=requests.get(endpoint)
            response=response.json()
            contests=response['result']
            ret=""
            for contest in contests:
                if contest['phase']=='FINISHED':
                    break
                else:
                    remTime=-contest['relativeTimeSeconds']
                    duration=contest['durationSeconds']
                    ret=ret+contest['name']+'\n'
                    ret=ret+"Duration"+(str(datetime.timedelta(seconds=duration)))+'\n'
                    ret=ret+"Starts in: "+str(datetime.timedelta(seconds=remTime))+'\n\n\n'
            # bot_handler.send_reply(message,ret)
            return ret
# handler_class = cfHandler