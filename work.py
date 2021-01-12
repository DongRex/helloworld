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
        
        sss="eyJwMV9SZXBvcnROdW0iOnsiVGV4dCI6IuaCqOW3sue0r+iuoeeUs+aKpTI5NuWkqSzov57nu63nlLPmiqUyOTPlpKkifSwicDFfQ2hlbmdOdW8iOnsiQ2hlY2tlZCI6dHJ1ZX0sInAxX0Jhb1NSUSI6eyJUZXh0IjoiMjAyMC0xMS0yNiJ9LCJwMV9HdW9OZWkiOnsiRl9JdGVtcyI6W1si5pivIiwi5pivKFllcykiLDFdLFsi5ZCmIiwi5ZCmKE5vKSIsMV1dLCJTZWxlY3RlZFZhbHVlIjoi5pivIn0sInAxX0RhbmdRU1RaSyI6eyJGX0l0ZW1zIjpbWyLoia/lpb0iLCLoia/lpb0oR29vZCkiLDFdLFsi5LiN6YCCIiwi5LiN6YCCKFNpY2spIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLoia/lpb0ifSwicDFfWmhlbmdaaHVhbmciOnsiRl9JdGVtcyI6W1si5oSf5YaSIiwi5oSf5YaSKENvbGQpIiwxXSxbIuWSs+WXvSIsIuWSs+WXvShDb3VnaCkiLDFdLFsi5Y+R54OtIiwi5Y+R54OtKEZldmVyKSIsMV1dLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdLCJIaWRkZW4iOnRydWV9LCJwMV9UaVdlbiI6eyJUZXh0IjoiMzYuNSJ9LCJwMV9Ib3NwaXRhbFN0YXR1cyI6eyJGX0l0ZW1zIjpbWyLlvoXlsLHljLsiLCLlvoXlsLHljLsoV2FpdGluZyBmb3IgbWVkaWNhbCB0cmVhdG1lbnQpIiwxXSxbIuW3sumalOemuyIsIuW3sumalOemuyhRdWFyYW50aW5lZCkiLDFdXSwiU2VsZWN0ZWRWYWx1ZSI6IuW+heWwseWMuyJ9LCJwMV9aYWlYaWFvIjp7IlNlbGVjdGVkVmFsdWUiOiLkvY/moKEiLCJGX0l0ZW1zIjpbWyLlsYXlrrYiLCLlsYXlrrYoSG9tZSkiLDFdLFsi5L2P5qChIiwi5L2P5qChKENhbXB1cykiLDFdLFsi5YW25LuWIiwi5YW25LuWKE90aGVyKSIsMV1dfSwicDFfRGFuZ1FERCI6eyJTZWxlY3RlZFZhbHVlIjoi5ZCmIiwiRl9JdGVtcyI6W1si5pivIiwi5pivIiwxXSxbIuWQpiIsIuWQpiIsMV1dfSwicDFfRGFuZ2Vyb3VzUGxhY2VMaXN0Ijp7IkZfSXRlbXMiOltdLCJTZWxlY3RlZFZhbHVlQXJyYXkiOltdfSwicDFfU2hhbmdoYWkiOnsiSGlkZGVuIjp0cnVlfSwicDFfZGRsU2hlbmciOnsiRl9JdGVtcyI6W1siLTEiLCLpgInmi6nnnIHku70iLDEsIiIsIiJdLFsi5YyX5LqsIiwi5YyX5LqsIiwxLCIiLCIiXSxbIuWkqea0pSIsIuWkqea0pSIsMSwiIiwiIl0sWyLkuIrmtbciLCLkuIrmtbciLDEsIiIsIiJdLFsi6YeN5bqGIiwi6YeN5bqGIiwxLCIiLCIiXSxbIuays+WMlyIsIuays+WMlyIsMSwiIiwiIl0sWyLlsbHopb8iLCLlsbHopb8iLDEsIiIsIiJdLFsi6L695a6BIiwi6L695a6BIiwxLCIiLCIiXSxbIuWQieaelyIsIuWQieaelyIsMSwiIiwiIl0sWyLpu5HpvpnmsZ8iLCLpu5HpvpnmsZ8iLDEsIiIsIiJdLFsi5rGf6IuPIiwi5rGf6IuPIiwxLCIiLCIiXSxbIua1meaxnyIsIua1meaxnyIsMSwiIiwiIl0sWyLlronlvr0iLCLlronlvr0iLDEsIiIsIiJdLFsi56aP5bu6Iiwi56aP5bu6IiwxLCIiLCIiXSxbIuaxn+ilvyIsIuaxn+ilvyIsMSwiIiwiIl0sWyLlsbHkuJwiLCLlsbHkuJwiLDEsIiIsIiJdLFsi5rKz5Y2XIiwi5rKz5Y2XIiwxLCIiLCIiXSxbIua5luWMlyIsIua5luWMlyIsMSwiIiwiIl0sWyLmuZbljZciLCLmuZbljZciLDEsIiIsIiJdLFsi5bm/5LicIiwi5bm/5LicIiwxLCIiLCIiXSxbIua1t+WNlyIsIua1t+WNlyIsMSwiIiwiIl0sWyLlm5vlt50iLCLlm5vlt50iLDEsIiIsIiJdLFsi6LS15beeIiwi6LS15beeIiwxLCIiLCIiXSxbIuS6keWNlyIsIuS6keWNlyIsMSwiIiwiIl0sWyLpmZXopb8iLCLpmZXopb8iLDEsIiIsIiJdLFsi55SY6IKDIiwi55SY6IKDIiwxLCIiLCIiXSxbIumdkua1tyIsIumdkua1tyIsMSwiIiwiIl0sWyLlhoXokpnlj6QiLCLlhoXokpnlj6QiLDEsIiIsIiJdLFsi5bm/6KW/Iiwi5bm/6KW/IiwxLCIiLCIiXSxbIuilv+iXjyIsIuilv+iXjyIsMSwiIiwiIl0sWyLlroHlpI8iLCLlroHlpI8iLDEsIiIsIiJdLFsi5paw55aGIiwi5paw55aGIiwxLCIiLCIiXSxbIummmea4ryIsIummmea4ryIsMSwiIiwiIl0sWyLmvrPpl6giLCLmvrPpl6giLDEsIiIsIiJdLFsi5Y+w5rm+Iiwi5Y+w5rm+IiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLkuIrmtbciXX0sInAxX2RkbFNoaSI6eyJFbmFibGVkIjp0cnVlLCJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeW4giIsMSwiIiwiIl0sWyLkuIrmtbfluIIiLCLkuIrmtbfluIIiLDEsIiIsIiJdXSwiU2VsZWN0ZWRWYWx1ZUFycmF5IjpbIuS4iua1t+W4giJdfSwicDFfZGRsWGlhbiI6eyJFbmFibGVkIjp0cnVlLCJGX0l0ZW1zIjpbWyItMSIsIumAieaLqeWOv+WMuiIsMSwiIiwiIl0sWyLpu4TmtabljLoiLCLpu4TmtabljLoiLDEsIiIsIiJdLFsi5Y2i5rm+5Yy6Iiwi5Y2i5rm+5Yy6IiwxLCIiLCIiXSxbIuW+kOaxh+WMuiIsIuW+kOaxh+WMuiIsMSwiIiwiIl0sWyLplb/lroHljLoiLCLplb/lroHljLoiLDEsIiIsIiJdLFsi6Z2Z5a6J5Yy6Iiwi6Z2Z5a6J5Yy6IiwxLCIiLCIiXSxbIuaZrumZgOWMuiIsIuaZrumZgOWMuiIsMSwiIiwiIl0sWyLombnlj6PljLoiLCLombnlj6PljLoiLDEsIiIsIiJdLFsi5p2o5rWm5Yy6Iiwi5p2o5rWm5Yy6IiwxLCIiLCIiXSxbIuWuneWxseWMuiIsIuWuneWxseWMuiIsMSwiIiwiIl0sWyLpl7XooYzljLoiLCLpl7XooYzljLoiLDEsIiIsIiJdLFsi5ZiJ5a6a5Yy6Iiwi5ZiJ5a6a5Yy6IiwxLCIiLCIiXSxbIuadvuaxn+WMuiIsIuadvuaxn+WMuiIsMSwiIiwiIl0sWyLph5HlsbHljLoiLCLph5HlsbHljLoiLDEsIiIsIiJdLFsi6Z2S5rWm5Yy6Iiwi6Z2S5rWm5Yy6IiwxLCIiLCIiXSxbIuWliei0pOWMuiIsIuWliei0pOWMuiIsMSwiIiwiIl0sWyLmtabkuJzmlrDljLoiLCLmtabkuJzmlrDljLoiLDEsIiIsIiJdLFsi5bSH5piO5Y6/Iiwi5bSH5piO5Y6/IiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLmtabkuJzmlrDljLoiXX0sInAxX1hpYW5nWERaIjp7IlRleHQiOiLkuIrmtbfnrKzkuozlt6XkuJrlpKflraYifSwicDFfWWlYR0xaVCI6eyJTZWxlY3RlZFZhbHVlIjoi5LiN5pivIiwiRl9JdGVtcyI6W1si5LiN5pivIiwi5LiN5pivKE5vKSIsMV0sWyLmmK8iLCLmmK8oWUVTKSIsMV1dfSwicDFfWVhHTFN0YXR1cyI6eyJGX0l0ZW1zIjpbWyLlsYXlrrbpmpTnprsiLCLlsYXlrrbpmpTnprsiLDFdLFsi5oyH5a6a6ZqU56a754K5Iiwi5oyH5a6a6ZqU56a754K5IiwxXV0sIlNlbGVjdGVkVmFsdWUiOiLlsYXlrrbpmpTnprsifSwicDFfWGluWEdaQkRHUloiOnsiU2VsZWN0ZWRWYWx1ZSI6IuacquWBmuajgOa1iyIsIkZfSXRlbXMiOltbIuacquWBmuajgOa1iyIsIuacquWBmuajgOa1iyIsMV0sWyLpmLPmgKciLCLpmLPmgKciLDFdLFsi6Zi05oCnIiwi6Zi05oCnIiwxXV19LCJwMV9RdWVaSFpKQyI6eyJGX0l0ZW1zIjpbWyLmmK8iLCLmmK8oWWVzKSIsMSwiIiwiIl0sWyLlkKYiLCLlkKYoTm8pIiwxLCIiLCIiXV0sIlNlbGVjdGVkVmFsdWVBcnJheSI6WyLlkKYiXX0sInAxX0ppYW9UR0oiOnsiU2VsZWN0ZWRWYWx1ZSI6IuWcqOayqiIsIkZfSXRlbXMiOltbIuWcqOayqiIsIuWcqOayqihJbiBTaGFuZ2hhaSkiLDFdLFsi5pyq5a6aIiwi5pyq5a6aKFVuZGV0ZXJtaW5lZCkiLDFdLFsi6aOe5py6Iiwi6aOe5py6KFBsYW5lKSIsMV0sWyLngavovaYiLCLngavovaYoVHJhaW4pIiwxXSxbIumVv+mAlOaxvei9piIsIumVv+mAlOaxvei9pihDb2FjaCkiLDFdLFsi56eB5a626L2m5oiW5YW25LuWIiwi56eB5a626L2m5oiW5YW25LuWKENhciBvciBvdGhlcnMpIiwxXV19LCJwMV9DZW5nRldIIjp7IkxhYmVsIjoiMTHmnIgxMuaXpeiHszEx5pyIMjbml6XmmK/lkKblnKjkuK3pq5jpo47pmanljLrpgJfnlZnov4coSGF2ZSB5b3UgYmVlbiB0byBkYW5nZXJvdXMgYXJlYSBpbiB0aGUgcmVjZW50IDE0IGRheXMpIn0sInAxX0NlbmdGV0hfUmlRaSI6eyJIaWRkZW4iOnRydWV9LCJwMV9DZW5nRldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWVDaHUiOnsiTGFiZWwiOiIxMeaciDEy5pel6IezMTHmnIgyNuaXpeaYr+WQpuS4juadpeiHquS4remrmOmjjumZqeWMuuWPkeeDreS6uuWRmOWvhuWIh+aOpeinpihEaWQgeW91IGhhdmUgY2xvc2UgY29udGFjdCB3aXRoIHBlb3BsZSBmcm9tIGRhbmdlcm91cyBhcmVhIGluIHRoZSByZWNlbnQgMTQgZGF5cz8pIn0sInAxX0ppZUNodV9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX0ppZUNodV9CZWlaaHUiOnsiSGlkZGVuIjp0cnVlfSwicDFfVHVKV0giOnsiTGFiZWwiOiIxMeaciDEy5pel6IezMTHmnIgyNuaXpeaYr+WQpuS5mOWdkOWFrOWFseS6pOmAmumAlOW+hOS4remrmOmjjumZqeWMuihEaWQgeW91IGhhdmUgdHJhdmVsIHZpYSBkYW5nZXJvdXMgYXJlYSBpbiB0aGUgcmVjZW50IDE0IGRheXM/KSJ9LCJwMV9UdUpXSF9SaVFpIjp7IkhpZGRlbiI6dHJ1ZX0sInAxX1R1SldIX0JlaVpodSI6eyJIaWRkZW4iOnRydWV9LCJwMV9KaWFSZW4iOnsiTGFiZWwiOiIxMeaciDEy5pel6IezMTHmnIgyNuaXpeWutuS6uuaYr+WQpuacieWPkeeDreetieeXh+eKtihEaWQgYW55IG9mIHlvdXIgZmFtaWx5IG1lbWJlcnMgaGF2ZSBzeW1wdG9tcyBzdWNoIGFzIGZldmVyLGV0YyBpbiB0aGUgcmVjZW50IDE0IGRheXM/KSJ9LCJwMV9KaWFSZW5fQmVpWmh1Ijp7IkhpZGRlbiI6dHJ1ZX0sInAxIjp7IklGcmFtZUF0dHJpYnV0ZXMiOnt9fX0="
        t=time.strftime("%Y-%m-%d",time.localtime())
        data = {
            "__EVENTTARGET":"p1$ctl00$btnSubmit",
            "p1$TiWen":"36",
            "p1$BaoSRQ":t,
            "F_STATE":sss,
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
       
db = pymysql.connect("localhost","report","cxd20000103","report" )
cursor = db.cursor()
sql = "SELECT username,password,email,state FROM user order by id desc"
cursor.execute(sql)
result = cursor.fetchall()
for i in result:
    pas=AES_Decrypt(key,i[1])
    login(i[0],pas)
    # print(i[0]+" "+pas)
cursor.close()
db.close()
# login('20191112520','cxd034912')


