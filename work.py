#coding=utf-8
#  开发团队    :  方舟
#  开发人员    :  Rex
#  开发时间    :  2020/5/20  23:01
#  开发名称    :  sss.py
#  开发工具    :  PyCharm
import re
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
import requests
import sys
import pymysql
from datetime import datetime
# import json
import urllib
import time

from email.header import Header
import smtplib
from Crypto.Cipher import AES
import os
from Crypto import Random
import base64

# 密钥（key）, 密斯偏移量（iv） CBC模式加密
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
vi = '' #偏移量
key = ''#密钥与php设置对应才行


def AES_Encrypt(key, data):
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
    enctext = encodestrs.decode('utf8')
    return enctext


def AES_Decrypt(key, data):
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    # 去补位
    text_decrypted = unpad(text_decrypted)
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


from_addr='1329092285@qq.com'   #邮件发送账号
qqCode='hpbnrlsdksptichj'   #授权码（这个要填自己获取到的）
smtp_server='smtp.qq.com'#固定写死
smtp_port=465#固定端口
stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
stmp.login(from_addr,qqCode)



def sendfalse(email,user):
    # 组装发送内容
    to_addrs = email  # 接收邮件账号
    message = MIMEText('', 'plain', 'utf-8')  # 发送的内容
    message['From'] = Header('', 'utf-8')  # 发件人
    message['To'] = Header(user, 'utf-8')  # 收件人
    subject = '每日一报提醒小助手：失败'
    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
    try:
        stmp.sendmail(from_addr, to_addrs, message.as_string())
        print(user+'NO')
    except Exception as e:
        print('邮件发送失败--' + str(e))


# chrome模块 默认不开启
def work(user,pa,email):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get('https://hsm.sspu.edu.cn/selfreport/Default.aspx')
        browser.maximize_window()
        browser.find_element_by_id('username').click()
        time.sleep(2)
        browser.find_element_by_id("username").send_keys(user)
        browser.find_element_by_id("password").send_keys(pa)
        browser.find_element_by_class_name('submit_button').click()
        time.sleep(2)
        browser.find_element_by_class_name('icos').click()
        time.sleep(2)
        browser.find_element_by_id("p1_TiWen-inputEl").send_keys("36.5")
        time.sleep(2)
        browser.find_element_by_class_name('f-btn-text').click()
        time.sleep(2)
        browser.find_element_by_id('fineui_24').click()
        time.sleep(2)
        browser.quit()
    except:
        time.sleep(15)
        sendfalse(email,user)
        return




def login(username, password):
    try:
        sessions = requests.Session();
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        header = {
            # "Referer": "https://id.sspu.edu.cn/cas/login?service=https%3a%2f%2fhsm.sspu.edu.cn%2fselfreport%2fLoginSSO.aspx%3ftargetUrl%3d%7bbase64%7daHR0cHM6Ly9oc20uc3NwdS5lZHUuY24vc2VsZnJlcG9ydC9JbmRleC5hc3B4",
            "User-Agent": userAgent,
            # "Cache-control": "private",
            "Origin": "https://id.sspu.edu.cn"}
        page = sessions.get(
            url="https://id.sspu.edu.cn/cas/login?service=https%3a%2f%2fhsm.sspu.edu.cn%2fselfreport%2fLoginSSO.aspx%3ftargetUrl%3d%7bbase64%7daHR0cHM6Ly9oc20uc3NwdS5lZHUuY24vc2VsZnJlcG9ydC9JbmRleC5hc3B4",
            headers=header)
        st = re.findall(r'<input type="hidden" name="lt" value="(.*)"/>', page.text)
        sst = "".join(st)
        data = {
            "username": username,
            "password": password,
            "_eventId": "submit",
            "errors": "0",
            "lt": sst}
        url = "https://id.sspu.edu.cn/cas/login?service=https%3a%2f%2fhsm.sspu.edu.cn%2fselfreport%2fLoginSSO.aspx%3ftargetUrl%3d%7bbase64%7daHR0cHM6Ly9oc20uc3NwdS5lZHUuY24vc2VsZnJlcG9ydC9JbmRleC5hc3B4"
        sessions.post(url=url, data=data, headers=header)
        
        basekey=""//提交内容
        t=time.strftime("%Y-%m-%d",time.localtime())
        data = {
            "__EVENTTARGET":"p1$ctl00$btnSubmit",
            "p1$TiWen":"36",
            "p1$BaoSRQ":t,
            "F_STATE":basekey,
        }
        url="https://hsm.sspu.edu.cn/selfreport/DayReport.aspx"
        page=sessions.post(url=url,data=data,headers=header)
        # print(page.content.decode('utf-8'))
        sessions.close()
        f=re.findall(r"提交成功",page.content.decode('utf-8'))
        if(len(f)):
            print(username+"YES")
        else:
            print(username+"NO")
    except:
        # work(username,password,email)
	    print(username+"登录失败")
#批量每日一报
# db = pymysql.connect("localhost","","","" )
# cursor = db.cursor()
# sql = "SELECT username,password,email,state FROM user order by id desc"
# cursor.execute(sql)
# result = cursor.fetchall()
# for i in result:
#     pas=AES_Decrypt(key,i[1])
#     login(i[0],pas)
#     # print(i[0]+" "+pas)
# cursor.close()
# db.close()

#单个每日一报

# login('','')


