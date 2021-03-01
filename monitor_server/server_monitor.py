import os
import time
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import configparser
import math
import datetime
from bottle import template
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SERVER_PATH = './'
CONFIG_FILE = './server_monitor.ini'
LOG_FILE_PATH = './'
INTERVAL = 5
SECONDS_OF_MIN = 60


def isProcessAlive(aliveCmd):
    # print('aliveCmd: ' + aliveCmd)
    logger.debug('aliveCmd: ' + aliveCmd)
    ret = os.system(aliveCmd)
    return ret == 0


def startProcess(startCmd):
    ret = os.system(startCmd)
    logger.info('system cmd:{} , ret:{}'.format(startCmd, ret))


def create_html(info_items, the_day):
    html = """
<html>
	<title>消息统计</title>
	<body>
		<br></br>
		<h2 align=center>报警消息({{date}})</h2>
		<table width="90%" align=center border="0" bgcolor="#666666" cellpadding="8>
			<tr bgcolor="#DDDDDD">
				<th>IP地址</th>
				<th>进程名称</th>
				<th>所属类型</th>
				<th>详细描述</th>
				<th>时间</th>
			</tr>
			<tr align=center bgcolor="#FFFFFF">
				<td><font color="#33CC00">{{items[0]}}</font></td>
				<td><font color="#33CC00">{{items[1]}}</font></td>
				<td><font color="#33CC00">{{items[2]}}</font></td>
				<td><font color="#33CC00">{{items[3]}}</font></td>
				<td><font color="#33CC00">{{items[4]}}</font></td>
			</tr>
		</table>
	</body>
</html>
    """
    return template(html, items=info_items, date=the_day)


def sendMail(cfg, process, content):
    logger.info('sendMail ' + process + ", content: " + content)
    return
    ret = True
    ipAddr = cfg.get("DEFAULT", "ipAddr")
    receivers = cfg.get("DEFAULT", "receivers")
    sender = cfg.get("DEFAULT", "sender")
    passwd = cfg.get("DEFAULT", "passwd")
    smtp_server = cfg.get("DEFAULT", "smtp_server")
    smtp_port = cfg.get("DEFAULT", "smtp_port")
    subject = cfg.get("DEFAULT", "subject")

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    item = [ipAddr, process, 'process_monitor', content, nowTime]
    # print(item)
    html = create_html(item, nowTime)
    msg = MIMEText(html, 'html', 'utf-8')  # 网页格式
    msg['From'] = formataddr([sender, sender])  # 括号里对应发件人邮箱昵称,发件人邮箱账号
    msg['To'] = ";".join([receivers])
    msg['Subject'] = subject
    receivers_1 = receivers.split(',')
    # print(receivers_1)

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender, passwd)
        server.sendmail(sender, receivers_1, msg.as_string())
        server.quit()
    except Exception as e:
        # print(e)
        logger.error(e)


def monitorProcess(process, cfg, state):
    logger.info("monitor_process: " + str(process) + " state: " + str(state))
    # 进程拉起失败后降低监控频率
    if not state['isAlive'] and state['skipTimes'] < math.pow(2, state['startTimes']) and state['skipTimes'] < 10:
        state['skipTimes'] += 1
        return

    if isProcessAlive(cfg.get(process, 'aliveCmd')):
        state['isAlive'] = True
        state['startTimes'] = 0
        state['skipTimes'] = 0
        return

    logger.info(process + ' is not alive and restarting...')
    # print(process + ' is not alive and restarting...')
    startProcess(cfg.get(process, 'startCmd'))
    time.sleep(2)

    if isProcessAlive(cfg.get(process, 'aliveCmd')):
        logger.info('restart ' + process + ' succeed')
        # print('start ' + process + ' succeed')
        sendMail(cfg, process, process + ' died, restart ok')
        state['alive'] = True
        state['startTimes'] = 0
        state['skipTimes'] = 0
    else:
        logger.info('restart ' + process + ' failed')
        # print('start ' + process + ' failed')
        now = int(time.time())
        if state['isAlive'] or now > state['lastReportTime'] + SECONDS_OF_MIN * cfg.getint(process, 'reportInterval'):
            sendMail(cfg, process, process + ' died, restart failed')
            state['lastReportTime'] = now
        state['isAlive'] = False
        state['startTimes'] += 1
        state['skipTimes'] = 1


def getLogger():
    logger = logging.getLogger('server_monitor')
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    logFileName = LOG_FILE_PATH + 'server_monitor.log'

    dailyFH = TimedRotatingFileHandler(filename=logFileName, when='MIDNIGHT', interval=1, backupCount=30)
    dailyFH.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(process)d|%(funcName)s|%(lineno)d|%(message)s')
    dailyFH.setFormatter(formatter)

    logger.propagate = False
    logger.addHandler(dailyFH)

    return logger


def processInstance():
    ret = os.popen('ps -ef | grep "server_monitor.py" | grep -v grep | grep -v sudo | wc -l').read().strip(' ')
    if ret != str(1):
        print('another instace running, ret: ' + str(ret))
        sys.exit(1)


if __name__ == '__main__':
    # processInstance() # 本服务监控
    try:
        logger = getLogger()
    except Exception as e:
        print(e)
        sys.exit(1)
    os.chdir(SERVER_PATH)

    logger.info('loading config...')
    cfg = configparser.SafeConfigParser()
    try:
        cfg.read(CONFIG_FILE, encoding='utf-8')
    except Exception as e:
        logger.error('read config failed:' + str(e))
        # print('read config failed:' + str(e))

    stateDict = dict({})
    for process in cfg.sections():
        stateDict[process] = dict({
            'isAlive': True,
            'startTimes': 0,
            'skipTimes': 0,
            'lastReportTime': 0,
        })

    logger.info('stateDict: %s' % stateDict.items())
    # print('stateDict: %s' % stateDict.items())

    logger.info('starting monitor\n\n')
    sendMail(cfg, 'server_monitor', 'server_monitor start...')
    while True:
        for process in cfg.sections():
            # print('process: ' + process)
            monitorProcess(process, cfg, stateDict[process])
            time.sleep(INTERVAL)
    logger.info('end monitoring')
    sys.exit(0)
