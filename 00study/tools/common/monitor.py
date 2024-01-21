# 用Python实现检测服务存活并启动(通用)
import subprocess
import sys

cmd = "netstat -lntup|grep 0.0.0.0:%s|grep tcp|wc -l" % sys.argv[1]
startNginx = 'docker start nginx'


def runCmd(result):
    obj = subprocess.Popen(result, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _port = obj.stdout.read().decode('gbk')

    return _port


def startCmd(port: int):
    """
    默认启动Nginx
    """
    if port == 0:
        print('服务未启动!!!')
        runCmd(startNginx)
        if int(runCmd(cmd)) == 0:
            print('启动失败!!!')
        else:
            print('启动成功')
    else:
        print('服务正常')


if __name__ == '__main__':
    port = int(runCmd(cmd))
    print(port)
    startCmd(port)
