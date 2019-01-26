import requests,json
from typing import Dict,Any

class mathHandler(object):
    def usage(self):
        return '''
            Get your mathematics expressions evaluated quickly :)
        '''
    def handle_message(self,message:Dict[str,str],bot_handler:Any)->None:
        print(message['content'])
        data=message['content'].split()
        if data[0]=="evaluate":
            expressions=data[1:]
            query={"expr":expressions,"precision":10}
            endpoint="http://api.mathjs.org/v4/"
            response = requests.post(endpoint,data=json.dumps(query))
            # print(response.json())
            answers = response.json()
            if answers['error']!=None:
                bot_handler.send_reply(message,answers['error'])
            else:
                ret=""
                for ans in answers['result']:
                    ret=ret+ans+'\n\n'
                bot_handler.send_reply(message,ret)
handler_class = mathHandler