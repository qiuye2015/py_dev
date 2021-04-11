# coding:utf-8
# fjp

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr


# 只可以给一个人发送邮件
class EmailClient():
    def __init__(self, receivers):
        self.receivers = receivers
        self.sender = 'qiuye_tju@163.com'
        self.subject = "Come On CHina"

        # 第三方 SMTP 服务
        self.mail_user = 'qiuye_tju@163.com'
        self.mail_pass = 'yes7585151'  # 授权码

    def format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self, content, subtype='plain'):
        message = MIMEText(content, subtype, 'utf-8')

        message['From'] = self.format_addr('qiuye_tju<%s>' % self.sender)
        message['To'] = self.format_addr('Me<%s>' % self.receivers)
        message['Subject'] = Header(self.subject, 'utf-8').encode()

        try:
            smtp = smtplib.SMTP(host='smtp.163.com', port=25)
            print('connect...')
            smtp.login(self.mail_user, self.mail_pass)
            print('login...')
            smtp.sendmail(self.sender, [self.receivers], message.as_string())
            print('SUCCESS...')
            smtp.quit()
        except smtplib.SMTPException as e:
            print('Error:' + format(e))


def main():
    #sender = 'f1119345739@163.com'
    emailclient = EmailClient(sender)
   # content = """
   # <html>
    #    <body>
     #       <h1>Hello</h1>
      #      <p>send by <a href="http://www.python.org">Python</a>...</p>
      #  </body>
    #</html>
    #"""
    content = "明天不上班"
    emailclient.send(content)
    #emailclient.send(content, 'html')


if __name__ == '__main__':
    main()




