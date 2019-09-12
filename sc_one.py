from selenium import webdriver

import credentials

import time

driver = webdriver.Chrome(executable_path = r'C:\chromedriver_win32\chromedriver.exe')

url = 'https://epaper.timesgroup.com/olive/apa/timesofindia/#panel=document'

driver.get(url)

driver.implicitly_wait(10)

driver.find_element_by_xpath("//a[@class='btn btn-primary']").click()

driver.implicitly_wait(10)

driver.switch_to_frame('plenigoFrameoverlay')

driver.find_element_by_id("email").send_keys(email)
driver.find_element_by_id("password").send_keys(password)

driver.find_element_by_css_selector(".btn.btn-default.pl-button").click()

time.sleep(5)

driver.switch_to_default_content()

driver.implicitly_wait(10)

driver.quit()