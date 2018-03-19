from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()
url = "http://devwww.kunlunhealth.com.cn/user/login"
driver.get(url)
driver.find_element_by_id("mobile").send_keys("15921709039")

driver.find_element_by_id("password").send_keys("asd123")
#time.sleep(1)
driver.find_element_by_name("submitForm").click()
time.sleep(3)

while True:
        curpage_url = driver.current_url
        print curpage_url
        if curpage_url != url:
            print 'Login finished!'
            break
        else:
            print u'wrong pwd'
            break

driver.close()
