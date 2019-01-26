import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def fblogin(bot_handler,message):
	if len(message)>=2:
		e=message[0]
		p=message[1]
		driver = webdriver.Chrome('/home/jugtaram/Downloads/chromedriver/chromedriver')  
		driver.get('http://www.google.com/xhtml')
		time.sleep(1)
		search_box = driver.find_element_by_name('q')
		search_box.send_keys('fb')
		search_box.submit()
		time.sleep(1)
		fblink=driver.find_element_by_link_text('facebook.com')
		type(fblink)
		time.sleep(1)
		fblink.click()
		time.sleep(1)
		form=driver.find_element_by_id('login_form')
		email=driver.find_element_by_name('email')
		password=driver.find_element_by_name('pass')
		email.send_keys(e)
		password.send_keys(p)
		time.sleep(1)
		form.submit()
		return "fb login successfully."
	else:
	    return "login <mobile no.> <password> :)" 
