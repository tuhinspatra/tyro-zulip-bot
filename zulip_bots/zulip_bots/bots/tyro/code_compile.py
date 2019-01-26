import os


def compile_code(bot_handler,message):
	if message['content'][3:6]=="cpp":
		RUN_URL = u'http://api.hackerearth.com/code/run/'
		CLIENT_SECRET = '7e91b5497d469d41490cd12acf2f6bef4765a337'
		source = message['content'][6:-3]
		code_file = open('code.cpp','w')
		code_file.write(source)
		code_file.close()
		os.system('bash shell.sh')
		if os.path.getsize('status.txt') == 0:
		    res = "**no compilation error**\n\n** output **\n"
		    os.system('./a.out 0< testcases.txt 1> status.txt')
		    file_code = open('status.txt','r')
		    res += file_code.read()
		    file_code.close()   
		else:
		    file_code= open('status.txt','r')
		    res = file_code.read()
		    file_code.close()

	else:
	    print(message['content'][4:-3]) 
	    RUN_URL = u'http://api.hackerearth.com/code/run/'
	    CLIENT_SECRET = '7e91b5497d469d41490cd12acf2f6bef4765a337'
	    source = message['content'][4:-3]
	    code_file = open('code.c','w')
	    code_file.write(source)
	    code_file.close()
	    os.system('bash shell2.sh')
	    if os.path.getsize('status.txt') == 0:
	    	res = "**no compilation error**\n\n** output **\n"
	    	os.system('./a.out 0< testcases.txt 1> status.txt')
	    	file_code = open('status.txt','r')
	    	res += file_code.read()
	    	file_code.close()    
	    else:
	        file_code= open('status.txt','r')
	        res = file_code.read()
	        file_code.close()
	return res