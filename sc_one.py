from selenium import webdriver

import credentials as cr

from bs4 import BeautifulSoup
import xlwt
import time
def check(string, sub_str): 
	if (string.find(sub_str) == -1): 
		return False
	else: 
		return True 
			
def getAllID(html,st):
	soup = BeautifulSoup(html,'lxml')
	driver.implicitly_wait(10)
	div = soup.find_all('div', class_ = 'block')
	out = []
	for i in div:
		if check(i.get("id"), "Ar") and check(i.get("id"), st):
			out.append(i.get("id"))			
	return out
workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('My Worksheet')

driver = webdriver.Chrome(executable_path = r'C:\chromedriver_win32\chromedriver.exe')

driver.implicitly_wait(30)

url = 'https://epaper.timesgroup.com/olive/apa/timesofindia/#panel=document'

driver.get(url)

driver.implicitly_wait(10)

driver.find_element_by_xpath("//a[@class='btn btn-primary']").click()

driver.implicitly_wait(10)

driver.switch_to_frame('plenigoFrameoverlay')

driver.find_element_by_id("email").send_keys(cr.email)
driver.find_element_by_id("password").send_keys(cr.password)

driver.find_element_by_css_selector(".btn.btn-default.pl-button").click()

time.sleep(5)

driver.switch_to_default_content()

driver.implicitly_wait(10)

url2 = "https://epaper.timesgroup.com/olive/apa/timesofindia/#panel=browse"

driver.get(url2)

driver.implicitly_wait(10)

time.sleep(10)

driver.find_element_by_xpath("//div[@class='side-bar']//div//div//div[@class='dropdown publications']//select").send_keys("T")

driver.implicitly_wait(10)

time.sleep(10)

driver.find_element_by_xpath("//li[contains(text(),'2018')]").click()

driver.implicitly_wait(30)

time.sleep(10)

driver.find_element_by_xpath("//li[contains(text(),'January')]").click()

driver.implicitly_wait(30)

time.sleep(10)

driver.find_element_by_xpath("//li[1]//div[2]").click()

# driver.find_element_by_xpath("//li[1]//div[2]").click()

driver.implicitly_wait(10)

time.sleep(15)

ht = driver.page_source

id = getAllID(ht,"0_1")

driver.implicitly_wait(19)

time.sleep(15)

print id

flag = 0
for i in id : 
	try:
		htm = driver.page_source
		driver.implicitly_wait(5)
		time.sleep(5)
		driver.find_element_by_xpath("//div[@id='" + i +"']").click()
		driver.implicitly_wait(5)
		time.sleep(5)
		htm = driver.page_source
		soup = BeautifulSoup(htm,'lxml')
		head = soup.find("h1",class_ = "headline")
		content = soup.find("div",class_ = "Content")
		if(head and content):
			allP = content.findChildren()
			print head.text
			finalP = ""
			for P in allP:
				finalP += P.text + "\n"
			time.sleep(5)
			worksheet.write(flag, 1,  head.text)
			worksheet.write(flag, 2,  finalP)
			driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
		else:
			time.sleep(3)
			driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
	finally:
		print(i)
		flag += 1

driver.implicitly_wait(10)

driver.find_element_by_xpath("//span[@class='gotoNextScreen']").click()

driver.implicitly_wait(10)

time.sleep(5)

for x in range(2,16):
	stri = "0_"
	newHTML = driver.page_source
	y = str(x)
	stri = stri+y
	newID = getAllID(newHTML,stri)
	print newID
	for k in newID:
		try:
			driver.implicitly_wait(5)
			driver.find_element_by_xpath("//div[@id='" + k +"']").click()
			driver.implicitly_wait(5)
			time.sleep(5)
			h = driver.page_source
			soup = BeautifulSoup(h,'lxml')
			head2 = soup.find("h1",class_ = "headline")
			content2 = soup.find("div",class_ = "Content")
			if(head2 and content2):
				allP2 = content2.findChildren()
				print head2.text
				finalP2 = ""
				for r in allP2:
					finalP2 += r.text + "\n"
				time.sleep(5)
				worksheet.write(flag,1,head2.text)
				worksheet.write(flag,2,finalP2)
				driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
			else:
				time.sleep(3)
				driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
		except:
				print "lol I avoided you stupid"
		finally:
			print(k)
			flag+=1
	if (x % 2 == 1):
		driver.find_element_by_xpath("//span[@class='gotoNextScreen']").click()		

workbook.save('Excel_Workbook.xls')
driver.quit()