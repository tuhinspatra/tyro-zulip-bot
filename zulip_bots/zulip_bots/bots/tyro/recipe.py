from watson_developer_cloud import VisualRecognitionV3, WatsonApiException
from os.path import abspath
import zulip,requests

def get_recipe(bot_handler,message):
	client = zulip.Client(config_file="./zuliprc")
	fp = open(message[1], 'rb')
	result = client.call_endpoint(
	'user_uploads',
	method='POST',
	files=[fp]
	)
	print(result)
	service = VisualRecognitionV3(
	'2018-03-19',
	url='https://gateway.watsonplatform.net/visual-recognition/api',
	iam_apikey='eJQk3lLSkE192AX96--I4yVVaPWdt6G1qNv1IP_0u7wv')
	file_path = abspath(message[1])
	with open(file_path, 'rb') as images_file:
		file_results = service.classify(
		    images_file=images_file,
		    threshold='0.1',
		    classifier_ids=['default']
		    ).get_result()
	recipe_query = ""
	i=0
	for word in file_results['images'][0]['classifiers'][0]['classes']:  
	    recipe_query += " "+word['class']
	    i = i+1
	    if i==3:
	        break

	print(recipe_query)
	recipe_res = requests.get("https://api.edamam.com/search?q="+recipe_query+"&app_id=468a2a5e&app_key=d8139dd0f416fe28158bbc88632ea13a").json()

	rec_res =''
	i=0 
	for recipe in recipe_res['hits']:
	    rec_res += '\n\n\n\n\n'+str(i+1)+'. **'+recipe['recipe']['label']+'**\n\n'+ recipe['recipe']['image']+'\n'
	    i=i+1
	    if i==3:
	        break
	final_res = {'url':"https://testbot.zulipchat.com"+result['uri'],'recipe':rec_res}

	# bot_handler.send_reply(message,"https://testbot.zulipchat.com"+result['uri'])            
	return final_res	

# elif query == "celeb":
#                 client = zulip.Client(config_file="./zuliprc")
#                 fp = open(data[1], 'rb')
#                 result = client.call_endpoint(
#                     'user_uploads',
#                     method='POST',
#                     files=[fp]
#                     )
#                 clients = SightengineClient('1853195251', 'ZRTWJ7FVXqwbtTBVa4u7')
#                 output = clients.check('celebrities').set_file(data[1])
#                 #print(output)
#                 bot_handler.send_reply(message,"https://testbot.zulipchat.com"+result['uri'])
#                 bot_handler.send_reply(message,"face_detection result says ::\n**"+output['faces'][0]['celebrity'][0]['name']+"**\n\n")
#                 res=requests.get('http://google.com/search?q='+output['faces'][0]['celebrity'][0]['name'])
#                 res.raise_for_status()
#                 obj=bs4.BeautifulSoup(res.text)
#                 result=obj.select('.r a')
#                 google_res = "**Googling...**\n"
#                 loop=min(3,len(result))
#                 j=0
#                 for i in range(loop):
#                     j = j+1
#                     google_res += str(j)+' **'+result[i].getText()+'**\n  http://google.com'+result[i].get('href')+'\n\n\n'
#                 bot_handler.send_reply(message,google_res)



	# if query == 'gif':
 #                client = zulip.Client(config_file="./zuliprc")
 #                fp = open(data[1], 'rb')
 #                result = client.call_endpoint(
 #                    'user_uploads',
 #                    method='POST',
 #                    files=[fp]
 #                    )
 #                print(result)
 #                service = VisualRecognitionV3(
 #                    '2018-03-19',
 #                    url='https://gateway.watsonplatform.net/visual-recognition/api',
 #                    iam_apikey='eJQk3lLSkE192AX96--I4yVVaPWdt6G1qNv1IP_0u7wv')
 #                file_path = abspath(data[1])
 #                with open(file_path, 'rb') as images_file:
 #                    file_results = service.classify(
 #                        images_file=images_file,
 #                        threshold='0.1',
 #                        classifier_ids=['default']
 #                        ).get_result()
 #                giphy_query = ""
 #                i=0    
 #                for word in file_results['images'][0]['classifiers'][0]['classes']:  
 #                    i += 1
 #                    if i==6:
 #                        break
 #                    giphy_query += " "+word['class']

 #                print(giphy_query)
 #                giphy_link = requests.get('https://api.giphy.com/v1/gifs/search?api_key=20YHBquZWWl4rkBaCVlfqE9xARU4D746&q='+giphy_query+'&limit=25&offset=0&rating=G&lang=en').json()
 #                res = ''
 #                i=0    #        i = 0
 #                #print(giphy_link['data'])
 #                for article in giphy_link['data']:      
 #                    res = res + article['images']['fixed_width']['mp4']+'\n\n'
 #                    #res = res +'https://giphy.com/media/'+article['id']+'/giphy.gif'+ "\n"
 #                    i += 1
 #                    if i == 5:
 #                        break
 #                bot_handler.send_reply(message,res)
 #                bot_handler.send_reply(message,"https://testbot.zulipchat.com"+result['uri'])
