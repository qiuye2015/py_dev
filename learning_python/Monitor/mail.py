#!/usr/bin/env python
# coding:utf8

'''
封装发送邮件
'''

import smtplib
from email.mime.text import MIMEText

HIGH_PRIORITY_MAIL = '1'
NORMAL_MAIL = '3'
LOW_PRIORITY_MAIL = '5'


class Mail(object):

    '''
    发送邮件
    '''

    def __init__(self, mail_host='mail.dangdang.com', mail_user='',
                 mail_pass='', port=25):
        self.host = mail_host
        self.port = port
        self.user = mail_user
        self.passwd = mail_pass
        self.server = None

    def connect(self, auth=False):
        '''
        连接邮件服务器
        '''
        self.server = smtplib.SMTP(self.host, self.port)
        self.server.ehlo()
        if auth:
            self.server.login(self.user, self.passwd)

    def send_mail(self, from_addr, to_list, sub,
                  content, priority=NORMAL_MAIL):
        '''
        to_list:发给谁
        sub:主题
        content:内容
        '''
        self.connect()
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['from'] = from_addr
        msg['To'] = ";".join(to_list)
        msg['X-Priority'] = priority

        mail_flag = False
        try:
            self.server.sendmail(
                from_addr, to_list, msg.as_string())
            mail_flag = True
        except Exception, e:
            print(e)
        finally:
            self.server.close()
        return mail_flag


def gen_recipient_addr(mail_str):
    '''
    获取收件人列表
    '''
    mail_lst = []
    for email_addr in mail_str.split(','):
        email_addr = email_addr.strip()
        if '@' not in email_addr:
            email_addr += '@dangdang.com'
        mail_lst.append(email_addr)
    return mail_lst


if __name__=="__main__":

    addressor="monitor@10.5.25.150"
    recipient=gen_recipient_addr("fujianpeng")
    content="failed"
    priority = HIGH_PRIORITY_MAIL
    headline="Monitor Process"

    mailManager = Mail()
    succ = mailManager.send_mail(addressor, recipient, headline, content, priority)

    if not succ:
        print("Send Mail Failed")
    else:
        print("Send Mail Success")

