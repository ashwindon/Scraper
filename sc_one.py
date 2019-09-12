from selenium import webdriver

import credentials as cr

import time

driver = webdriver.Chrome(executable_path = r'C:\chromedriver_win32\chromedriver.exe')

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

driver.find_element_by_xpath("//div[@class='side-bar']//div//div//div[@class='dropdown publications']//select").send_keys("TTTTTTTTTTTTTTTTTTT")

time.sleep(7)

driver.find_element_by_xpath("//li[contains(text(),'2018')]").click()

time.sleep(7)

driver.find_element_by_xpath("//li[contains(text(),'January')]").click()

time.sleep(5)

driver.find_element_by_xpath("//li[1]//div[2]").click()

time.sleep(15)

driver.quit()