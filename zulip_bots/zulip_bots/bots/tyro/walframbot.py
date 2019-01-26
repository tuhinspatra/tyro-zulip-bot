import requests
from requests.exceptions import HTTPError,ConnectionError
from typing import Dict, Any
import json

WALFRAM_API_URL="http://api.wolframalpha.com/v1/result"
API_KEY="73KWR2-WKYXVRETG6"
class WalframHandler(object):
    
    def usage(self):
        return '''What you wanna know today? Ask me :) '''

    def handle_message(self,message:Dict[str,str],bot_handler:Any)->None:
        print(message["content"])
        query=message["content"]
        query=query.strip()
        pars={'appid':API_KEY,'i':query}
        data=requests.get(WALFRAM_API_URL,pars)
        # json.dumps(data)
        print(data.text)
        bot_handler.send_reply(message,data.text)
handler_class=WalframHandler