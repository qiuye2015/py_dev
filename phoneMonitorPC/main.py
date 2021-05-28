import os
import time
import yagmail
from imbox import Imbox
from PIL import ImageGrab


def send_mail(sender, to, contents):
    smtp = yagmail.SMTP(user=sender, host='smtp.163.com')
    smtp.send(to, subject='Remote Control', contents=contents)


def read_mail(username, password):
    with Imbox('imap.163.com', username, password, ssl=True) as box:
        all_msg = box.messages(unread=True)
        for uid, message in all_msg:
            # 如果是手机端发来的远程控制邮件
            if message.subject == 'Remote Control':
                # 标记为已读
                box.mark_seen(uid)
                return message.body['plain'][0]


def shutdown():
    # 关机
    os.system('shutdown -s -t 0')


def grab(sender, to):
    # 截取电脑全屏
    surface = ImageGrab.grab()
    # 将截屏保存为surface.jpg
    surface.save('surface.jpg')
    # 将截屏发送给手机
    send_mail(sender, to, ['surface.jpg'])


def main():
    # 电脑用来发送邮件已经电脑读取的邮箱
    username = 'sockwz@163.com'
    password = '你的授权码'
    # 手机端的邮箱
    receiver = '2930777518@qq.com'
    # 读取邮件的时间间隔
    time_space = 5
    # 注册账户
    yagmail.register(username, password)
    while True:
        # 读取未读邮件
        msg = read_mail(username, password)
        if msg:
            # 根据不同的内容执行不同操作
            if msg == 'shutdown':
                shutdown()
            elif msg == 'grab':
                grab(username, receiver)
        time.sleep(time_space)


if __name__ == '__main__':
    main()