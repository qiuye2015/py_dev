from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class QianPiaoSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'D:\software\chromedriver.exe')

        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.login_succ_url = "https://kyfw.12306.cn/otn/view/index.html"

        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
        self.confirmPassenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def _wait_input(self):
        # self.from_station = input("出发地:")
        # self.to_station = input("目的地:")
        # self.depart_time = input("出发时间:")
        # self.passengers = input("乘客姓名(如有多个乘客,用英文逗号隔开):").split(",")
        # self.trains = input("车次,若有多个车次,用英文逗号隔开:").split(",")

        self.from_station = "北京"
        self.to_station = "天津"
        self.depart_time = "2021-07-24"
        self.passengers = ['付建鹏']
        self.trains = ['C2551']

        print(self.from_station)
        print(self.to_station)
        print(self.depart_time)
        print(self.passengers)
        print(self.trains)

    def _login(self):
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.login_succ_url))
        print("登录成功")
        print("*" * 30)

    def _order_ticket(self):
        # 1. 跳转到查询余票界面
        self.driver.get(self.search_url)
        # 2. 等待出发地是否输入正确
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "fromStationText"), self.from_station))
        # 3. 等待目的地是否输入正确
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.to_station))
        # 4. 等待出发日期书否输入正确
        WebDriverWait(self.driver, 1000).until(
            EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time))
        # 5. 等待查询按钮是否可用
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.ID, "query_ticket")))

        # 6. 如果能够被点击了,那么就找到这个查询按钮,执行点击事件
        searchBtn = self.driver.find_element_by_id("query_ticket")
        searchBtn.click()
        # 7. 等待车次信息显示出来
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.XPATH, ".//tbody[@id='queryLeftTable']/tr")))
        # WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.XPATH, "//*[@id='queryLeftTable']/tr")))

        # 8. 找到所有没有datatran属性的tr标签,这些标签是存储了车次信息的
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")

        # 9. 遍历所有满足条件的车次信息
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            print("车次判断:",train_number)
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[4]").text  # 4表示二等座
                if left_ticket == "有" or left_ticket.isdigit:
                    print(train_number + "有票")
                    print("=" * 30)
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()
                    # 等待是否来到确认乘客信息页面
                    WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.confirmPassenger_url))

                    # 等待所有乘客信息加载完成
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.XPATH, ".//ul[@id='normal_passenger_id']/li")))
                    # 获取所有乘客信息
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()
                    # 获取提交订单的按钮
                    submitBtn = self.driver.find_element_by_id("submitOrder_id")
                    submitBtn.click()
                    # 显示等待 确认订单的对话框是否已经出现
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "dhtmlx_wins_body_outer")))
                    # 显示等待 确认订单按钮已经出现,执行点击操作
                    WebDriverWait(self.driver, 1000).until(
                        EC.presence_of_element_located((By.ID, "qr_submit_id")))

                    confimBtn = self.driver.find_element_by_id("qr_submit_id")
                    confimBtn.click()
                    # while confimBtn:
                    #     confimBtn.click()
                    #     confimBtn = self.driver.find_element_by_id("qr_submit_id")
                    print("*" * 30)
                    print("抢购成功")

    def run(self):
        self._wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = QianPiaoSpider()
    spider.run()
