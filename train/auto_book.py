# -*- coding: utf-8 -*-
'''2017年春运火车票抢票
火车票预订时间对照：
1月25日（廿八） 12月27日
1月26日（廿九） 12月28日
1月27日（除夕） 12月29日
2月1日（初四）1月3日
2月2日（初五）1月4日
2月3日（初六）1月5日
2月4日（初七）1月6日
碰到的问题
一个账户在未支付情况下无法购买别的车票
添加购票入联系人
连续登入n次不成功自动重启
各铁路局电话订票和互联网售票时间变更为7：00～23：00，预售期仍保持12天（含购票当日）
TODO:
4.23  后续实现数据库控制买票流程，虚拟机运行，集群控制运行
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import Select

import time
import urllib
import urllib2
import json
from PIL import Image
from StringIO import StringIO

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def login_proc(sel,username, password):
    # 打开登录页面

    login_url = 'https://kyfw.12306.cn/otn/login/init'
    sel.get(login_url)
    # sign in the username
    time.sleep(2)
    uc_url='https://kyfw.12306.cn/otn/index/initMy12306'
    if(sel.current_url==uc_url):
        return True

    try:
        user_input = sel.find_element_by_id("username")
        user_input.clear()
        user_input.send_keys(username)
    except:
        sel.close()
        print 'user-id write error!'
    # sign in the pasword
    try:
        pwd_input = sel.find_element_by_id("password")
        pwd_input.clear()
        pwd_input.send_keys(password)
    except:
        sel.close()
        print 'pw write error!'
    checkTime = 0
    while True:
        try:
            time.sleep(4)
            checkTime = checkTime+1
            print u'进行第'+str(checkTime)+u'次登入'
            element=sel.find_element_by_class_name("touclick-image")
            image_url = sel.find_element_by_class_name("touclick-image").get_attribute("src")
            if len(image_url)!=0:
                # print 'getCapthaImageUrl:'+image_url

                sel.save_screenshot('tmp.png')

                # print(element.location)                # 打印元素坐标
                # print(element.size)                    # 打印元素大小
                left = element.location['x']
                top = element.location['y']
                right = element.location['x'] + element.size['width']
                bottom = element.location['y'] + element.size['height']
                im = Image.open('tmp.png')
                im = im.crop((left*2, top*2, right*2, bottom*2))
                s = StringIO()
                im.save(s,format='png')
                # print s.getvalue()
                # im.save('tmp.png')


                # resp = urllib.urlopen(image_url)
                check_img = bytearray(s.getvalue())

                req = urllib2.Request('http://www.youyouwosi.cn:8001/yyws/Ocr')
                req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
                req.add_header("Cookie", "uid=a00110")
                try:
                    f=urllib2.urlopen(req, data=check_img,timeout=200)

                    resImageData=f.read().decode('utf-8')
                    print(u'返回解析数据:', resImageData)
                    dataJson=json.loads(resImageData)
                    if dataJson['result']==True :
                        coordinate=dataJson['data']['val']
                        # print u'获取坐标'+coordinate
                        coordinate=coordinate.replace("&",",")
                        cr=coordinate.split(',')
                        for i in range(len(cr)):
                            # print i,cr[i]
                            if i%2 :
                                cr[i]=int(cr[i])//2-32
                            else:
                                cr[i]=int(cr[i])//2-12
                        coordinate=','.join(str(i) for i in cr)
                        print u'转换后坐标'+coordinate
                        #根据返回坐标模拟点击
                        js = 'document.getElementById("randCode").value="'+coordinate+'";'
                        #print u'执行js'+js
                        sel.execute_script(js)
                        time.sleep(1)

                        # print u'点击登入按钮'
                        sel.find_element_by_id('loginSub').click()
                        time.sleep(7)

                        #判断登入成功
                        if sel.current_url != login_url and sel.current_url[:-1] != login_url:  # choose wrong verify_pic
                            print 'Login finished!'
                            break
                        else:
                            print 'Login failed'
                    else:
                        print u'解析图片失败重试'
                        sel.find_element_by_class_name("touclick-reload").click()
                except Exception as e:
                    print e
                    print u'服务响应码解析失败'
            else:
                print u'未找到验证图片，关闭进程'
                sel.close()
                break
        except Exception as e:
            print e
        # finally :
        #     print 'login page finished!'
        # break


    # while True:
    #     time.sleep(10)
    #     print 'test'


    # Check for Login success
    # while True:
    #     curpage_url = sel.current_url
    #     if curpage_url != login_url:
    #         if curpage_url[:-1] != login_url:  # choose wrong verify_pic
    #             print 'Login finished!'
    #             break
    #     else:
    #         sel.close()
    #         time.sleep(5)
    #         print u'------------>等待用户图片验证'
    return True


def search_proc(sel,fromStation,toStation,dateStation,train_type='', timer=False):
    # print u'--------->选择车次类型', train_type
    # 定时抢票时间点
    if timer == True:
        while True:
            current_time = time.localtime()
            if ((current_time.tm_hour == 14) and (current_time.tm_min >= 25) and (
                        current_time.tm_sec >= 00)):
                print u'开始刷票...'
                break
            else:
                time.sleep(5)
                if current_time.tm_sec % 30 == 0:
                    print time.strftime('%H:%M:%S', current_time)


    # 打开订票网页

    book_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    # sel.get(book_url)
    while True:
        if(sel.current_url==book_url):
            print 'enter search page'
            break
        else:
            print 'waiting enter search page'
            sel.find_element_by_xpath("//li[@id='selectYuding']").find_elements_by_tag_name("a")[0].click()
            time.sleep(2)

    # 始发站
    # sel.find_element_by_id('fromStationText').click()
    # from_station = sel.find_element_by_xpath('//*[@id="ul_list1"]/li[32]') # 深圳
    # from_station.click()
    sel.add_cookie({"name": "_jc_save_fromStation", "value": fromStation})
    # 终点站
    # sel.find_element_by_id('toStationText').click()
    # sel.find_element_by_id('nav_list3').click()#点击事件
    # tation = sel.find_element_by_xpath('//*[@id="ul_list1"]/li[9]') # 广州
    # to_station.click()
    sel.add_cookie({"name": "_jc_save_toStation", "value": toStation})
    # 出发日期
    # date_sel = sel.find_element_by_id('train_date')
    # js = "document.getElementById('train_date').removeAttribute('readonly')" # del train_date readonly property
    # sel.execute_script(js)
    # date_sel.clear()
    # date_sel.send_keys(leave_date)
    sel.add_cookie({"name": "_jc_save_fromDate", "value": dateStation})
    sel.refresh()
    # 车次类型选择
    # train_type_dict = {'T': '//input[@name="cc_type" and @value="T"]',  # 特快
    #                    'G': '//input[@name="cc_type" and @value="G"]',  # 高铁
    #                    'D': '//input[@name="cc_type" and @value="D"]',  # 动车
    #                    'Z': '//input[@name="cc_type" and @value="Z"]'}  # 直达
    # if train_type == 'T' or train_type == 'G' or train_type == 'D' or train_type == 'Z':
    #     sel.find_element_by_xpath(train_type_dict[train_type]).click()
    # else:
    #     print u"车次类型异常或未选择!(train_type=%s)" % train_type


def book_proc(sel,train_no, seat_type,apply_name,refresh_interval=0):
    # 等待状态查询
    #商务TZ 9 一等 ZY M   二等  ZE 0  高级软卧 GR 软卧 RW 4  动卧 SRRB F 硬卧 YW 3 软座 RZ  硬座 YZ 1
    seat_type_dict= {'TZ':'9',
                     'ZY':'M',
                     'ZE':'0',
                     'GR':'',
                     'RW':'4',
                     'SRRB':'F',
                     'YW':'3',
                     'RZ':'',
                     'YZ':'1' }
    query_times = 0
    time_begin = time.time()
    while True:
        current_time = time.localtime()

        if( current_time.tm_hour <7 or  ( current_time.tm_hour>22 and current_time.tm_min>50)):
            print 'not in sale time'
            return False

        # 循环查询
        time.sleep(refresh_interval)
        # 开始查询 @id="ZE_6c000D281201"
        try:

            search_btn = WebDriverWait(sel, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="query_ticket"]')))
            time.sleep(2)
            search_btn.click()
        except:
            print 'search btn wrong,continue'
            continue

        while True:
        # 扫描查询结果
            try:
                # T17
                tic_tb_item = WebDriverWait(sel, 20).until( EC.presence_of_element_located((By.XPATH, '//*[@id="'+seat_type+'_'+train_no+'"]')))
                # G381
                # tic_tb_item = WebDriverWait(sel,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ZE_240000G38107"]')))
                tic_ava_num = tic_tb_item.text
                break
            except:  # 应对查询按钮一次点击后,网站未返回查询结果
                search_btn.click()

        print u'票数查询结果:'+tic_ava_num

        if tic_ava_num == u'无' or tic_ava_num == u'*':  # 无票或未开售
            query_times += 1
            time_cur = time.time()
            print u'第%d次查询,总计耗时%s秒' % (query_times, time_cur - time_begin)
            continue
        else:
            # 订票 @id="ticket_6c000D281201"
            # sel.find_element_by_xpath('//*[@id="ticket_240000G38107"]/td[13]/a').click()  # G381
            break
    # 判断页面跳是否转至乘客选择页面
    cust_sel_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'

    # 乘车人选择
    while True:
        time.sleep(1)

        if (sel.current_url == cust_sel_url):
            try:
                time.sleep(3)
                #选取第一个人
                print 'choose apply name'


                # print sel.find_element_by_xpath('//*[contains(text(),"常用联系人")]//u').get_attribute("title")
                # print sel.find_element_by_xpath('//label[contains(text(),"徐慧芳")]//u').text
                # apply_id=sel.find_element_by_xpath('//*[text(),"徐慧芳"]//u').get_attribute("for")
                # print apply_id
                # time.sleep(1000000)
                sel.find_element_by_xpath('//*[@id="normalPassenger_4"]').click()
                s1 = Select(sel.find_element_by_id('seatType_1'))  # 实例化Select
                s1.select_by_value(seat_type_dict[seat_type])
                break
            except Exception as e:
                print e
                print u'等待常用联系人列表...'
                time.sleep(1)
        else:
            try:
                print 'click  ticket'
                sel.find_element_by_xpath('//*[@id="ticket_'+train_no+'"]/td[13]/a').click()
                time.sleep(2)  # T17
            except:
                print 'pop login win'
                return False

    # 席别选择
    # 提交订票
    sel.find_element_by_xpath('//*[@id="submitOrder_id"]').click()
    # 确认订票信息
    while True:
        try:
            # sel.switch_to.frame(sel.find_element_by_xpath('//*[@id="body_id"]/iframe[1]'))
            sel.find_element_by_id("qr_submit_id").click()
            print 'create order '
            break
        except:
            print 'waiting check order'
            time.sleep(2)
    return True

def continue_pay(sel):
    try:
        sel.find_element_by_id("link_4_NonComOrder").click()
        time.sleep(2)
        sel.find_element_by_id("continuePayNoMyComplete").click()
    except:
        print 'waiting usercenter'
        time.sleep(2)
    return True


def pay_proc(sel,alipayName,alipayPwd):
    #支付
    while True:
        try:
            sel.find_element_by_id("payButton").click()
            time.sleep(4)
            handles = sel.window_handles # 获取当前窗口句柄集合（列表类型）
            sel.switch_to_window(handles[1])
            sel.find_elements_by_class_name("bank3_5")[8].find_elements_by_tag_name("img")[0].click()
            #跳转支付宝 https://mrexcashier.alipay.com
            break
        except:
            print 'waiting jump pay page'
            time.sleep(3)
        #进入支付页面
    time.sleep(2)
    pay_url = sel.current_url
    while True:
        try :
            sel.find_elements_by_id('J_tLoginId')[0].clear()
            sel.find_elements_by_id('J_tLoginId')[0].send_keys(alipayName)
            sel.find_elements_by_id('payPasswd_rsainput')[0].clear()
            sel.find_elements_by_id('payPasswd_rsainput')[0].send_keys(alipayPwd)
            time.sleep(2)

            sel.find_element_by_id("J_submitBtn").click()
            time.sleep(2)
            if sel.current_url!=pay_url:
                break

        except Exception as e:
            print e
            print 'waiting pay'
            time.sleep(2)

    #跳转收银台
    # print sel.find_elements_by_id('payPassword_input')[0].isDisplayed()
    # sel.find_elements_by_id('payPassword_input')[0].send_keys(alipayPwd)
    stage_url = sel.current_url
    while True:
        try :
            sel.find_elements_by_id('payPassword_rsainput')[0].clear()
            sel.find_elements_by_id('payPassword_rsainput')[0].send_keys(alipayPwd)
            time.sleep(1)
            sel.find_element_by_id("J_authSubmit").click()
            time.sleep(2)
            if  stage_url != sel.current_url:
                print 'pay success'
                return True
            else:
                print 'pay failed'
                return False

            break
        except Exception as e:
            print e
            print u'waiting final pay'
            time.sleep(2)



if __name__ == '__main__':
    # 变量定义
    alipayName='15921709039'
    alipayPwd='Feihide1234'
    leave_date = '2018-12-23'
    train_type = 'G'
    refresh_interval =1
    timer = False
    # value_fromstation = '%u5317%u4EAC%2CBJP'  # 始发站（深圳北）   天津
    # value_tostation =  '%u5929%u6D25%2CTJP'  #'%u4E0A%u6D77%2CSHH'  # 终点站（上海）
    # value_date = '2018-05-12'  # 出发时间
    # train_no =  '280000260415'  #'240000G1070H'
    # seat_type= 'YZ'     # 商务TZ 9 一等 ZY M   二等  ZE 0  高级软卧 GR 软卧 RW 4  动卧 SRRB F 硬卧 YW 3 软座 RZ  硬座 YZ 1 无座 WZ
    # apply_name= '徐慧芳'
    value_fromstation = '%u4E0A%u6D77%2CSHH'  # 始发站（深圳北）   天津
    value_tostation = u'汉口'+'%2C'+'HKN'  #'%u4E0A%u6D77%2CSHH'  # 终点站（上海）
    value_date = '2018-04-29'  # 出发时间
    train_no =  '550000D95600'  #'240000G1070H'
    seat_type= 'SRRB'     # 商务TZ 9 一等 ZY M   二等  ZE 0  高级软卧 GR 软卧 RW 4  动卧 SRRB F 硬卧 YW 3 软座 RZ  硬座 YZ 1 无座 WZ
    apply_name= '徐慧芳'
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/work/download"}
    chromeOptions.add_experimental_option("prefs", prefs)

    sel = webdriver.Chrome('/work/chromedriver',chrome_options=chromeOptions)
    # sel=webdriver.Firefox()
    sel.implicitly_wait(10)
    is_continue_pay=False
    while True:
        current_time = time.localtime()

        if( current_time.tm_hour <7 or  ( current_time.tm_hour>22 and current_time.tm_min>50)):
            print 'not in sale time on main'
            time.sleep(5*60)
            continue

        login_proc(sel,'feihide', 'hide1234')
        if is_continue_pay:
            book_result=continue_pay(sel)
        else:
            search_proc(sel,value_fromstation,value_tostation, value_date,train_type, timer)
            book_result=book_proc(sel, train_no,seat_type,apply_name,refresh_interval)

        if(book_result):
            pay_result=pay_proc(sel,alipayName,alipayPwd)
            if pay_result:
                print 'finished'
                break
            else:
                is_continue_pay=True
                continue
        else:
            print 'continue to login'

    sel.quit()
