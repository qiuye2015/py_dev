# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 2019/03/16
# 淘宝秒杀脚本，扫码登录版
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def login():
    # 打开淘宝登录页，并进行扫码登录
    browser.get("https://www.taobao.com")
    time.sleep(3)
    if browser.find_element(by=By.LINK_TEXT, value="亲，请登录"):
        browser.find_element(by=By.LINK_TEXT, value="亲，请登录").click()
        print("请在15秒内完成扫码")
        # time.sleep(15)
        browser.get("https://cart.taobao.com/cart.htm")
    # time.sleep(3)

    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(times, choose):
    # 点击购物车里全选按钮
    if choose == 2:
        print("请手动勾选需要购买的商品")
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now > times:
            if choose == 1:
                while True:
                    if browser.find_element(by=By.ID, value="J_SelectAll2"):
                        browser.find_element(by=By.ID, value="J_SelectAll2").click()
                        # 点击结算按钮
                        if browser.find_element(by=By.LINK_TEXT, value="结 算"):
                            browser.find_element(by=By.LINK_TEXT, value="结 算").click()
                            try:
                                if browser.find_element(by=By.LINK_TEXT, value='提交订单'):
                                    browser.find_element(by=By.LINK_TEXT, value='提交订单').click()
                                    now1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                    print("抢购成功时间：%s" % now1)
                                    break
                            except Exception as e:
                                print("再次尝试提交订单")
                            finally:
                                browser.get("https://cart.taobao.com/cart.htm")
                    time.sleep(0.01)


if __name__ == "__main__":
    # times = input("请输入抢购时间，格式如(2018-09-06 11:20:00.000000):")
    times = "2023-11-02 14:30:00.000000"
    # 时间格式："2018-09-06 11:20:00.000000"
    browser = webdriver.Chrome()
    # browser.maximize_window()
    login()
    # choose = int(input("到时间自动勾选购物车请输入“1”，否则输入“2”："))
    choose = 1
    buy(times, choose)
