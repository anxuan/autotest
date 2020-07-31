# -*- coding: utf-8 -*-
# @Time    : 2018/1/27 上午11:23
# @Author  : 宜信致诚，徐岩华
# @File    : send_mail_test.py
# @Software: PyCharm
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail():
    '''
    1、send_mail()函数以最简单的方式测试邮件发送
    2、建议使用mail.sina.com，其他的如163邮箱、126邮箱、qq邮箱，安全级别非常高，有许多垃圾邮件拦截策略，会让你的测试工作事倍功半
    3、
    '''
    # 发送者邮箱、用户名和密码，注：用户名和发送者邮箱一样
    sender = 'jackee1024@sina.com'
    username = 'jackee1024@sina.com'
    password = 'Wxd1024!'
    # 发送服务器设置
    smtp_server = 'smtp.sina.com'
    # 接收者，你的公司邮箱
    receiver = 'wangxudong1129@hupu.com'

    msg = MIMEText('这里有异常0', 'plain', 'utf-8')
    subject = 'CAT报警'
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.login(username, password)
    smtp.set_debuglevel(0)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('send succ....')


def send_post():

    params = {
        'from_addr': 'wangxudong1129@hupu.com',
        'to_addrs': 'wangxudong1129@hupu.com',  #  wangxudong1129@hupu.com
        'subject': 'cat alert',
        'smtp_server': 'smtp.exmail.qq.com',  # smtp.exmail.qq.com
        'content': 'cat error! 99999999',
        'username': 'wangxudong1129@hupu.com',
        'password': 'Wxd114418'
    }

    # url = 'http://129.211.123.211:9000/mail/'
    url = 'http://106.14.73.63:9000/mail/'
    # url = 'http://localhost:9000/mail/'
    r = requests.post(url, data=params)
    print(r.content)
    print(r.status_code)
    # s = '&'.join([k+'='+v for k, v in params.items()])
    # print(s)


if __name__ == '__main__':
    # send_mail()
    send_post()

    pass



