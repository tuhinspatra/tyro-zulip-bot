import requests,bs4,webbrowser

def get_result(bot_handler,message):
	if message[0] == "book": 
	    res=requests.get('https://books.google.com?q='+' '.join(message[1:]))
	    res.raise_for_status()
	    obj=bs4.BeautifulSoup(res.text)
	    result=obj.select('.r a')
	    book_res = "**Searching...**\n"
	    loop=min(3,len(result))
	    j=0
	    for i in range(loop):
	        j = j+1
	        book_res += str(j)+' '+'**'+result[i].getText()+'**\n'+result[i].get('href')+'\n\n\n'
	else:

	    book_res = 'Googling....'
	    res=requests.get('http://google.com/search?q='+' '.join(message[1:]))
	    res.raise_for_status()
	    obj=bs4.BeautifulSoup(res.text)
	    result=obj.select('.r a')
	    loop=min(3,len(result))
	    for i in range(loop):
	    	webbrowser.open('http://google.com'+result[i].get('href'))
	return book_res   
        