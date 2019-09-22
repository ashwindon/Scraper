from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import credentials as cr
from bs4 import BeautifulSoup
import xlwt
import time
import smtplib

#from selenium import webdriver
from selenium.webdriver.chrome.options import Options
folder = "data\\"
limit = 4
options = Options()
options.headless = True
# chrome_options=options
driver = webdriver.Chrome(executable_path = r'C:\chromedriver_win32\chromedriver.exe', chrome_options=options)

def report(msg):
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(cr.sender_email_id, cr.sender_email_id_password) 
	s.sendmail(cr.sender_email_id, cr.receiver_email_id, msg)
	s.quit() 

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

def getAllDays(html):
	soup = BeautifulSoup(html,'lxml')
	driver.implicitly_wait(10)
	ul = soup.find('ul',class_ = 'doclist')
	allDays = ul.findChildren("li")
	return allDays



#driver = webdriver.Chrome(executable_path = r'C:\chromedriver_win32\chromedriver.exe')

url = 'https://epaper.timesgroup.com/olive/apa/timesofindia/#panel=document'

driver.get(url)

time.sleep(9)

timeout = 30000

try:
	element_present = EC.presence_of_element_located((By.XPATH,"//a[@class='btn btn-primary']"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_xpath("//a[@class='btn btn-primary']").click()
except:
	print "Shit is slow 1"
	driver.quit()

try:
	element_present = EC.presence_of_element_located((By.ID,"plenigoFrameoverlay"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.switch_to_frame('plenigoFrameoverlay')
except:
	print "Shit is slow 2"
	driver.quit()

try:
	element_present = EC.presence_of_element_located((By.ID,"email"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_id("email").send_keys(cr.email)
except:
	print "Shit is slow 3"
	driver.quit()

try:
	element_present = EC.presence_of_element_located((By.ID,"password"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_id("password").send_keys(cr.password)
except:
	print "Shit is slow 4"
	driver.quit()

try:
	element_present = EC.presence_of_element_located((By.CSS_SELECTOR,".btn.btn-default.pl-button"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_css_selector(".btn.btn-default.pl-button").click()
except:
	print "Shit is slow 5"
	driver.quit()
	
driver.switch_to_default_content()

time.sleep(5)

url2 = "https://epaper.timesgroup.com/olive/apa/timesofindia/#panel=browse"

driver.get(url2)

time.sleep(5)

try:
	element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='side-bar']//div//div//div[@class='dropdown publications']//select"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_xpath("//div[@class='side-bar']//div//div//div[@class='dropdown publications']//select").send_keys("T")
except:
	print "Shit is slow 6"
	driver.quit()

time.sleep(5)
try:
	time.sleep(5)
	element_present = EC.presence_of_element_located((By.XPATH,"//li[contains(text(),'2018')]"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_xpath("//li[contains(text(),'2018')]").click()
except:
	print "Shit is slow 7"
	driver.quit()

time.sleep(5)
try:
	time.sleep(5)
	element_present = EC.presence_of_element_located((By.XPATH,"//li[contains(text(),'January')]"))
	WebDriverWait(driver, timeout).until(element_present)
	driver.find_element_by_xpath("//li[contains(text(),'January')]").click()
except:
	print "Shit is slow 8"
	driver.quit()

time.sleep(5)
Mpage = driver.page_source
#######
Days = getAllDays(Mpage)
time.sleep(5)
print Days
flag = 0
daycount = 1
newsdate = datetime.datetime(2018,1,1)

for d in Days:
	daycountstr = str(daycount)
	dateStr = str(newsdate.day)+ "/" + str(newsdate.month) + "/" + str(newsdate.year)
	workbook = xlwt.Workbook(encoding = 'ascii')
	worksheet = workbook.add_sheet('Sheet1')
	try:
		element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='day_list']//li["+daycountstr+"]"))
		WebDriverWait(driver, timeout).until(element_present)
		driver.find_element_by_xpath("//div[@class='day_list']//li["+daycountstr+"]").click()
	except:
		print "Shit is slow 9"
		driver.quit()
###############
	time.sleep(10)
	ht = driver.page_source
	
	id = getAllID(ht,"0_1")
	#########
	time.sleep(5)
	print id
	for i in id : 
		try:
			htm = driver.page_source
			try:
				element_present = EC.presence_of_element_located((By.XPATH,"//div[@id='" + i +"']"))
				WebDriverWait(driver, timeout).until(element_present)
				driver.find_element_by_xpath("//div[@id='" + i +"']").click()
			except:
				print "Shit is slow 10"
				
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
				worksheet.write(flag,0,dateStr)
				worksheet.write(flag,1,head.text)
				worksheet.write(flag,2,finalP)
				try:
					element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]"))
					WebDriverWait(driver, timeout).until(element_present)
					driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
				except:
					print "Shit is slow 11"
					
			else:
				try:
					element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]"))
					WebDriverWait(driver, timeout).until(element_present)
					driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
				except:
					print "Shit is slow 12"
						
		except:
			print "lol I avoided you fool!!!!!!!!"
		finally:
			print(i)
			workbook.save(folder + dateStr.replace("/", '-') + '.xls')
			flag += 1

	try:	
		driver.find_element_by_xpath("//span[@class='gotoNextScreen']").click()	
		time.sleep(5)		
		for x in range(2,limit):
			stri = "0_"
			newHTML = driver.page_source
			y = str(x)
			stri = stri+y
			newID = getAllID(newHTML,stri)
			print newID
			for k in newID:
				try:
					try:
						element_present = EC.presence_of_element_located((By.XPATH,"//div[@id='" + k +"']"))
						WebDriverWait(driver,timeout).until(element_present)
						driver.find_element_by_xpath("//div[@id='" + k +"']").click()
					except:
						print "Shit is slow 14"
						
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
						worksheet.write(flag,0,dateStr)
						worksheet.write(flag,1,head2.text)
						worksheet.write(flag,2,finalP2)
						try:
							element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]"))
							WebDriverWait(driver,timeout).until(element_present)
							driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
						except:
							print "Shit is slow 15"
								
					else:
						try:
							element_present = EC.presence_of_element_located((By.XPATH,"//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]"))
							WebDriverWait(driver,timeout).until(element_present)
							driver.find_element_by_xpath("//div[@class='right-important relative']//button[@class='dark-button'][contains(text(),'Close')]").click()
						except:
							print "Shit is slow 16"		
				except:
						print "lol I avoided you stupid"
				finally:
					print(k)
					workbook.save(folder +  dateStr.replace('/', '-') + '.xls')
					flag+=1
			if (x % 2 == 1):
				try:
					element_present = EC.presence_of_element_located((By.XPATH,"//span[@class='gotoNextScreen']"))
					WebDriverWait(driver,timeout).until(element_present)
					driver.find_element_by_xpath("//span[@class='gotoNextScreen']").click()
				except:
					print "Shit is slow 17"
					driver.quit()		
	except Exception as e:
		print "It was holiday!"
		print "\n"
		print e
		
	daycount += 1
	msg = dateStr + " is done!"
	report(msg)
	driver.execute_script("window.history.go(-1)")
	newsdate += datetime.timedelta(days=1)
	time.sleep(5)

#workbook.save('Excel_Workbook.xls')
driver.quit()