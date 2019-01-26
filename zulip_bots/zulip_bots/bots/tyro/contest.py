import requests,bs4

def get_contest(bot_handler,message):
	if message == "codechef":
	    res = "**runnig contest on codechef**\n"
	    res1=requests.get('https://www.codechef.com/contests')
	    res1.raise_for_status()
	    ccObj=bs4.BeautifulSoup(res1.text,"lxml")
	    datacode1=ccObj.select('.dataTable > tbody')
	    i=0
	    for con in datacode1:
	        res += con.getText()+'\n'
	        i = i+1
	        if i == 2:
	            break
	    return res

	elif message == "codeforces":
	    contest_res ="present contest on codeforces\n"
	    res2=requests.get('http://codeforces.com/contests')
	    res2.raise_for_status()
	    cfObj=bs4.BeautifulSoup(res2.text,"lxml")
	    datacode2=cfObj.select('#pageContent > div > div.datatable > div tr td')
	    for con in datacode2:
	        contest_res += con.getText()+'\n'
	    print(contest_res)
	    return contest_res
	elif message == "spoj":
	    spoj_res ="**spoj currently running contest**\n"
	    res3=requests.get('http://www.spoj.com/contests/')
	    res3.raise_for_status()
	    cfObj1=bs4.BeautifulSoup(res3.text,"lxml")
	    datacode3=cfObj1.select('#content > div > div')
	    for con in datacode3:
	        spoj_res += con.getText()+'\n'
	    print(spoj_res)
	    return spoj_res
	else:
		return "**no record available for this judge**"
