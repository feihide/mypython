from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
driver = webdriver.Chrome('/work/chromedriver')
url = "https://login.taobao.com/member/login.jhtml"
driver.get(url)
while True:
    try :
        driver.find_element_by_id("TPL_username_1").send_keys("15921709039")

        driver.find_element_by_id("TPL_password_1").send_keys("asd123")
        #time.sleep(1)
        driver.find_element_by_id("J_SubmitStatic").click()

    except Exception as e:
        print e
        print u'waiting'


# elem_pic = driver.find_element_by_xpath("//div[@class='help-item help-item-weixin']/img")
# print elem_pic.get_attribute("src")
# action = ActionChains(driver).move_to_element(elem_pic)
# action.context_click(elem_pic)
#
# action.send_keys(Keys.ARROW_DOWN)
# action.send_keys(Keys.ARROW_DOWN)
#
# time.sleep(3)
# action.send_keys('v')
# action.perform()


# alert.switch_to_alert()
# alert.accept()

#driver.find_element_by_name("submitForm").click()
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
