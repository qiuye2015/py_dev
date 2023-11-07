# -*- coding: utf-8 -*-
#
# 北京二手房购房资金计算
# 适用于: 北京二手商品房, 公房, 一类/二类经济适用房
# 资金单位: 万
# author: herrkaefer
# update: 2017.04.10

# 功能:
# - 针对买家能力, 计算其购买各类型房屋可承受上限
# - 针对某套房子:
#     - 考虑买家能力, 优化计算不同购房方案, 如:
#         - 最少初始准备资金
#         - 最小月供
#     - 不考虑资金约束, 计算购房方案

# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import font_manager

# 设定中文字体，否则保存图片中文是乱码
# myfont = font_manager.FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')

import datetime
from pprint import pprint


# 买家模型
class Buyer:
    def __init__(self):
        self.is_first = True  # 是否首套
        self.age = 30  # 买家年龄 (节点: 40)
        self.max_prepared_money = 600.0  # 初始总准备资金: 首付总资金 + 预留资金
        self.num_month_reserved = 12  # 预留多少个月的月供
        self.other_money_reserved = 20.0  # 其它预留资金
        self.max_monthly_repayment = 3.0  # 可承受月供上限 (贷款要求低于月收入一半)
        self.loan_from_fund_is_wanted = True  # 是否需要公积金贷款 (其余用商贷补充)
        # 设为False则全部商贷

    # 打印买家信息
    def print_info(self):
        print(
            "买家设定: %s, 年龄: %d, 准备资金: %.1f万, 预留月供: %d个月, 其它预留: %.1f万, 月供上限: %.1f万"
            % (
                "首套" if self.is_first else "二套",
                self.age,
                self.max_prepared_money,
                self.num_month_reserved,
                self.other_money_reserved,
                self.max_monthly_repayment,
            )
        )

    # 计算买家针对某种类型房子的可承受价格上限 (5万为最小区间, 更精确意义不大)
    def _cal_limit(self, house):
        house.print_info()
        house.print_header()

        max_impossible_price = int((self.max_prepared_money / 0.3 + 5) / 10) * 10.0
        price_list = generate_linspace(max_impossible_price, 10.0, -5.0)
        max_price = None
        cp_for_max_price = None

        for p in price_list:
            house.price = p
            contract_price_list = generate_linspace(house.evaluation_price(), house.lowest_price(), -0.5)
            min_prepared_money = house.price * 100
            contract_price = None
            for cp in contract_price_list:
                house.contract_price = cp
                prepared_money = house.total_prepared_money()
                # 资金允许且初始所需资金更少
                if house.is_buyable_for_current_contract_price() and prepared_money <= min_prepared_money:
                    min_prepared_money = prepared_money
                    contract_price = cp

            if contract_price is not None:  # 此价格可承受
                max_price = p
                cp_for_max_price = contract_price
                break

        if max_price is not None:
            house.price = max_price
            house.contract_price = cp_for_max_price
            house.print_item()

    # 计算买家可购买的各类型房屋上限 (当前版本只考虑五环内房屋)
    def cal_limits(self):
        self.print_info()
        house = House(self)

        ## 满五唯一公房
        print("=" * 92)
        house.type = "public"
        house.num_holding_years = 5
        house.is_only = True
        house.original_price = 0
        self._cal_limit(house)

        ## 满五不唯一公房
        print("-" * 92)
        house.type = "public"
        house.num_holding_years = 5
        house.is_only = False
        house.original_price = 0
        self._cal_limit(house)

        ## 满二公房
        print("-" * 92)
        house.type = "public"
        house.num_holding_years = 2
        house.is_only = False
        house.original_price = 0
        self._cal_limit(house)

        ## 不满二公房
        print("-" * 92)
        house.type = "public"
        house.num_holding_years = 1
        house.is_only = False
        house.original_price = 0
        self._cal_limit(house)

        ## 满五唯一二类经适房
        print("-" * 92)
        house.type = "affordable2"
        house.num_holding_years = 5
        house.is_only = True
        house.original_price = 0.0
        self._cal_limit(house)

        ## 满五不唯一二类经适房
        print("-" * 92)
        house.type = "affordable2"
        house.num_holding_years = 5
        house.is_only = False
        house.original_price = 0.0
        self._cal_limit(house)

        ## 满五唯一商品房
        print("-" * 92)
        house.type = "commercial"
        house.num_holding_years = 5
        house.is_only = True
        house.original_price = 100.0
        self._cal_limit(house)

        ## 满五不唯一商品房
        print("-" * 92)
        house.type = "commercial"
        house.num_holding_years = 5
        house.is_only = False
        house.original_price = 100.0
        self._cal_limit(house)

        ## 满二商品房
        print("-" * 92)
        house.type = "commercial"
        house.num_holding_years = 3
        house.is_only = False
        house.original_price = 200.0
        self._cal_limit(house)

        ## 不满二商品房
        print("-" * 92)
        house.type = "commercial"
        house.num_holding_years = 1
        house.is_only = False
        house.original_price = 200.0
        self._cal_limit(house)

        print("=" * 92 + "\n")


# 房屋模型
class House:
    def __init__(self, buyer):
        self.buyer = buyer

        # 房屋缺省参数
        self.type = "public"  # 房屋类型:
        # "commercial" (商品房),
        # "public" (已购公房),
        # "affordable1" (一类经适房)
        # "affordable2" (二类经适房)
        self.price = 530.0  # 实际成交价
        self.original_price = 0.0  # 房屋原值 (如果找不到, 设为0)
        self.num_holding_years = 5  # 房产证或契税票下发年数 (节点: 2, 5)
        self.is_only = False  # 是否业主 (家庭为单位) 在京唯一住房
        self.area = 40.0  # 房屋面积 (节点: 90, 140)
        self.building_year = 2000  # 建筑年代 (节点: 1992=>25年房龄)
        self.building_structure = "steel"  # 建筑结构: "steel": 钢混; "brick": 砖混
        self.position = 5  # 位置: 5: 5环内; 6: 5-6环; 7: 6环外
        self.floor_area_ratio = 1.5  # 小区容积率 (节点: 1.0)
        self.monthly_rent = 0.5  # 估计月租金 (如准备自住设为0)

        # 中介费率
        self.commission_rate = 0.027  # 链家

        # 评估
        self.evaluation_ratio = 0.85  # 评估价/成交价最大值, 0.85 ~ 0.9x/1.x

        # 网签价 (变量)
        self.contract_price = None

    # -------------------------------------------------------------------------

    # 房龄
    def age(self):
        return datetime.datetime.now().year - self.building_year

    # 是否普通住房: 同时满足三个条件
    def is_normal(self):
        if self.floor_area_ratio >= 1.0 and self.area < 140.0 and self.contract_price < self.max_normal_price():
            return True
        else:
            return False

    # 最低过户指导价 (核定价)
    # 按房价0.3估算, 实际应该按地区指导单价*面积, 但地区指导单价比较神秘, 按3万算
    def lowest_price(self):
        return min(3.0 * self.area, 0.3 * self.price)

    # 普通/非普通总价分界线
    def max_normal_price(self):
        if self.position == 5:
            return 468.0
        elif self.position == 6:
            return 374.4
        else:
            return 280.8

    # 评估价 (一般为网签最高价格)
    def evaluation_price(self):
        return self.price * self.evaluation_ratio

    # -------------------------------------------------------------------------
    # 贷款

    # 商贷比例
    def loan_bank_proportion(self):
        if self.buyer.is_first:
            return 0.65 if self.is_normal() else 0.6
        else:
            return 0.4 if self.is_normal() else 0.2  # 317新政

    # 贷款总额度
    def loan(self):
        assert self.contract_price is not None
        return float(int(self.contract_price * self.loan_bank_proportion()))

    # 公积金贷款利率
    def loan_fund_rate(self):
        if self.buyer.is_first:
            return 0.0325
        else:
            return 0.03575

    # 公积金贷款年限
    def loan_fund_years(self):
        bs_limit = 57 if self.building_structure == "steel" else 47
        return min(25, bs_limit - self.age(), 69 - self.buyer.age)

    # 公积金贷款总额 (粗略估计)
    def loan_from_fund(self):
        if self.buyer.loan_from_fund_is_wanted:
            lf = min(120.0 if self.buyer.is_first else 80.0, self.contract_price * 0.8, self.loan())  # 不超过总贷款额
            return float(int(lf))  # 一般抹去零头
        else:
            return 0.0

    # 商贷利率
    def loan_bank_rate(self):
        return 0.049 * (0.9 if self.buyer.is_first else 1.1)

    # 商贷年限
    def loan_bank_years(self):
        return min(25, 50 - self.age(), 65 - self.buyer.age)

    # 商贷总额
    def loan_from_bank(self):
        lb = self.loan() - self.loan_from_fund()
        assert lb >= 0
        return float(int(lb))  # 银行一般抹去零头

    # -------------------------------------------------------------------------
    # 税费, 中介费

    # 契税
    def deed_tax(self):
        # 契税税率
        if self.buyer.is_first:
            deed_tax_rate = 0.01 if self.area <= 90 else 0.015
        else:
            deed_tax_rate = 0.03

        if self.contract_price > self.lowest_price():
            return (self.contract_price - self.value_added_tax()) * deed_tax_rate
        else:
            return self.lowest_price() / 1.05 * deed_tax_rate

    # 增值税
    def value_added_tax(self):
        # 满2年的普通住宅/公房/二类经适房, 免征
        if self.num_holding_years >= 2 and (self.is_normal() or self.type == "public" or self.type == "affordable2"):
            return 0.0

        value_added_tax_rate = 0.056
        vat = 0.0

        tax_base = max(self.contract_price, self.lowest_price())
        # 不满2年
        if self.num_holding_years < 2:
            vat = tax_base / 1.05 * value_added_tax_rate

        # 满2年非普通
        else:
            if self.original_price > 0:  # 差额征收
                vat = (tax_base - self.original_price) / 1.05 * value_added_tax_rate
            else:  # 若原值找不到, 全额征收
                vat = tax_base / 1.05 * value_added_tax_rate

        return vat * 1.12  # 附加 12%

    # 个税
    def income_tax(self):
        # 满五唯一
        if self.num_holding_years >= 5 and self.is_only:
            return 0.0

        # 对公房, 原值设为不可追溯
        # if self.is_public:
        #     self.original_price = 0

        # 注: 下面的计算并不十分精确, 但误差可忽略

        # 原值可追溯: 差额20%
        if self.original_price > 0:
            if self.contract_price > self.lowest_price():
                return (
                    self.contract_price - self.original_price - self.value_added_tax() - self.contract_price * 0.1
                ) * 0.2
            else:
                return (self.lowest_price() / 1.05 - self.original_price - self.lowest_price() * 0.1) * 0.2
        # 原值不可追溯: 全额1%
        else:
            if self.contract_price > self.lowest_price():
                return (self.contract_price - self.value_added_tax()) * 0.01
            else:
                return self.lowest_price() / 1.05 * 0.01

    # 土地出让金(一类经适房) or 综合地价款(二类经适房): 商品房无, 公房可忽略
    def land_fee(self):
        if self.type == "affordable1":
            if self.building_year < 2008:  # 精确应为2008.04.11
                return 0.1 * max(self.contract_price, self.lowest_price())
            else:
                return 0.7 * (self.contract_price - self.original_price)
        elif self.type == "affordable2":
            return 0.03 * max(self.contract_price, self.lowest_price())
        else:
            return 0.0

    # 总税费
    def tax(self):
        return self.deed_tax() + self.value_added_tax() + self.income_tax() + self.land_fee()

    # 中介佣金
    def commission(self):
        return self.commission_rate * self.price

    # -------------------------------------------------------------------------
    # 首付

    # 房子首付
    def initial_payment_for_house(self):
        return self.price - self.loan()

    # 首付总款: 房屋首付 + 税 + 中介费
    def initial_payment(self):
        return self.initial_payment_for_house() + self.tax() + self.commission()

    # 所需初始准备总资金: 首付 + 预留 (还款按等额本息)
    def total_prepared_money(self):
        return (
            self.initial_payment()
            + self.buyer.num_month_reserved * self.monthly_repayment()
            - self.buyer.num_month_reserved * self.monthly_rent
            + self.buyer.other_money_reserved
        )

    # -------------------------------------------------------------------------
    # 还款计算: 等额本息

    # 商贷月供 (等额本息)
    def monthly_repayment_bank(self):
        R = self.loan_bank_rate() / 12  # 月利率
        n = self.loan_bank_years() * 12  # 还款期数
        Rn = (1 + R) ** n
        return self.loan_from_bank() * R * Rn / (Rn - 1)

    # 公积金贷款月供 (等额本息)
    def monthly_repayment_fund(self):
        if self.loan_from_fund() > 0:
            R = self.loan_fund_rate() / 12  # 月利率
            n = self.loan_fund_years() * 12  # 还款期数
            Rn = (1 + R) ** n
            return self.loan_from_fund() * R * Rn / (Rn - 1)
        else:
            return 0.0

    # 总月供 (等额本息)
    def monthly_repayment(self):
        return self.monthly_repayment_bank() + self.monthly_repayment_fund()

    # 商贷总利息 (等额本息)
    def total_interest_bank(self):
        return self.monthly_repayment_bank() * self.loan_bank_years() * 12 - self.loan_from_bank()

    # 公积金贷款总利息 (等额本息)
    def total_interest_fund(self):
        return self.monthly_repayment_fund() * self.loan_fund_years() * 12 - self.loan_from_fund()

    # 总利息 (等额本息)
    def total_interest(self):
        return self.total_interest_bank() + self.total_interest_fund()

    # 应付总款: (等额本息)
    def total_payment(self):
        return (
            self.initial_payment()
            + self.monthly_repayment_bank() * self.loan_bank_years() * 12
            + self.monthly_repayment_fund() * self.loan_fund_years() * 12
        )

    # -------------------------------------------------------------------------
    # 还款计算: 等额本金

    # 月供银行贷款 (等额本金)
    def monthly_repayment_bank_equal_principal(self):
        n = self.loan_bank_years() * 12
        monthly_principal = self.loan_from_bank() / n
        R = self.loan_bank_rate() / 12
        monthly_repayment = []
        for i in range(n):
            interest = (self.loan_from_bank() - monthly_principal * i) * R
            monthly_repayment.append(monthly_principal + interest)
        num_years = max(self.loan_bank_years(), self.loan_fund_years())
        if len(monthly_repayment) < num_years:
            monthly_repayment.extend([0] * (num_years - len(monthly_repayment)))
        return monthly_repayment

    # 月供公积金贷款 (等额本金)
    def monthly_repayment_fund_equal_principal(self):
        n = self.loan_fund_years() * 12
        monthly_principal = self.loan_from_fund() / n
        R = self.loan_fund_rate() / 12
        monthly_repayment = []
        for i in range(n):
            interest = (self.loan_from_fund() - monthly_principal * i) * R
            monthly_repayment.append(monthly_principal + interest)
        num_years = max(self.loan_bank_years(), self.loan_fund_years())
        if len(monthly_repayment) < num_years:
            monthly_repayment.extend([0] * (num_years - len(monthly_repayment)))
        return monthly_repayment

    # 总月供 (等额本金)
    def monthly_repayment_equal_principal(self):
        repayment_bank = self.monthly_repayment_bank_equal_principal()
        repayment_fund = self.monthly_repayment_fund_equal_principal()
        monthly_repayment = []
        for i in range(max(len(repayment_bank), len(repayment_fund))):
            monthly_repayment.append(repayment_bank[i] + repayment_fund[i])
        return monthly_repayment

    # 商贷总利息 (等额本金)
    def total_interest_bank_equal_principal(self):
        return sum(self.monthly_repayment_bank_equal_principal()) - self.loan_from_bank()

    # 公积金贷款总利息 (等额本金)
    def total_interest_fund_equal_principal(self):
        return sum(self.monthly_repayment_fund_equal_principal()) - self.loan_from_fund()

    # 总利息 (等额本金)
    def total_interest_equal_principal(self):
        return self.total_interest_bank_equal_principal() + self.total_interest_fund_equal_principal()

    # 应付总款 (等额本金)
    def total_payment_equal_principal(self):
        return (
            self.initial_payment()
            + sum(self.monthly_repayment_bank_equal_principal())
            + sum(self.monthly_repayment_fund_equal_principal())
        )

    # -------------------------------------------------------------------------

    # 以当前设定的网签价, 买家是否买得起此房
    def is_buyable_for_current_contract_price(self):
        if (
            self.total_prepared_money() <= self.buyer.max_prepared_money
            and self.monthly_repayment() <= self.buyer.max_monthly_repayment
        ):
            return True
        else:
            return False

    # 通过遍历可行网签价, 判断买家资金是否允许购买此房, 并给出各种优化指标下的购房方案
    def cal_plans(self):
        self.buyer.print_info()
        self.print_info()
        print('-' * 40)

        # 考虑买家能力的方案
        is_buyable = False
        min_prepared_money = self.price * 100.0
        cp_min_prepared_money = None
        min_monthly_repayment = self.buyer.max_monthly_repayment * 2.0
        cp_min_monthly_repayment = None

        # 不考虑资金限制的方案
        g_min_prepared_money = self.price * 100.0
        g_cp_min_prepared_money = None

        contract_price_list = generate_linspace(self.lowest_price(), self.evaluation_price(), 0.1)

        for cp in contract_price_list:
            self.contract_price = cp

            prepared_money = self.total_prepared_money()
            monthly_repayment = self.monthly_repayment()

            if prepared_money < g_min_prepared_money:
                g_min_prepared_money = prepared_money
                g_cp_min_prepared_money = cp

            if self.is_buyable_for_current_contract_price():
                is_buyable = True

                if prepared_money < min_prepared_money:
                    min_prepared_money = prepared_money
                    cp_min_prepared_money = cp

                if monthly_repayment < min_monthly_repayment:
                    min_monthly_repayment = monthly_repayment
                    cp_min_monthly_repayment = cp

        if is_buyable:
            print("此房买得起, 下面是购房方案:\n")
            print("==> 最低首备资金方案:")
            self.contract_price = cp_min_prepared_money
            self.print_header()
            self.print_item()

            print("\n==> 最低月供方案 (贷款仍按最大比例最长年限):")
            self.contract_price = cp_min_monthly_repayment
            self.print_header()
            self.print_item()
        else:
            print("\n此房买不起. 下面是不考虑资金限制的购房方案:\n")
            print("==> 最低首备资金方案:")
            self.contract_price = g_cp_min_prepared_money
            self.print_header()
            self.print_item()

    # -------------------------------------------------------------------------

    # 打印房屋信息
    def print_info(self):
        print(
            "房屋类型: %s%s%s, 原值: %.1f万, 面积: %.1f平, 房龄: %d年, 估计月租: %.2f万"
            % (
                "满五" if self.num_holding_years >= 5 else ("满二" if self.num_holding_years >= 2 else "不满二"),
                "唯一" if self.is_only else "不唯一",
                "公房" if self.type == "public" else ("商品房" if self.type == "commercial" else "二类经适房"),
                self.original_price,
                self.area,
                self.age(),
                self.monthly_rent,
            )
        )

    def print_header(self):
        print("成交价\t网签价\t首备\t首付\t贷\t\t\t首(房)\t税(契+增+个+地)\t\t\t中介\t月供")

    def print_item(self):
        print(
            "%.1f\t%.1f\t%.1f\t%.1f\t公%.0f(%d) + 商%.0f(%d)\t%.1f\t%.1f (%4.1f+%4.1f+%4.1f+%4.1f)\t%.1f\t%4.2f (%.2f+%.2f)"
            % (
                self.price,
                self.contract_price,
                self.total_prepared_money(),
                self.initial_payment(),
                self.loan_from_fund(),
                self.loan_fund_years(),
                self.loan_from_bank(),
                self.loan_bank_years(),
                self.initial_payment_for_house(),
                self.tax(),
                self.deed_tax(),
                self.value_added_tax(),
                self.income_tax(),
                self.land_fee(),
                self.commission(),
                self.monthly_repayment(),
                self.monthly_repayment_fund(),
                self.monthly_repayment_bank(),
            )
        )


# 等差列表生成 (一定包含端点值)
def generate_linspace(startv, endv, step):
    if step == 0:
        return [startv]

    re = []
    p = startv

    if step > 0:
        while p < endv:
            re.append(p)
            p = p + step
    else:
        while p > endv:
            re.append(p)
            p = p + step

    re.append(endv)
    return re


if __name__ == '__main__':
    # 针对某买家计算
    buyer = Buyer()
    buyer.is_first = True  # 是否首套
    buyer.age = 32  # 买家年龄
    buyer.num_month_reserved = 24  # 预留多少个月的月供
    buyer.other_money_reserved = 20.0  # 其它预留资金
    buyer.max_prepared_money = 800.0  # 初始总资金
    buyer.max_monthly_repayment = 3.0  # 可承受月供上限
    buyer.loan_from_fund_is_wanted = True  # 是否需要公积金贷款
    buyer.cal_limits()

    # 针对某套房子计算
    house = House(buyer)
    house.type = "commercial"
    house.price = 1000.0  # 实际成交价 (节点: 468.0)
    house.original_price = 200.0  # 房屋原值 (如果找不到, 设为0)
    house.num_holding_years = 5  # 房产证或契税票下发年数 (节点: 2, 5)
    house.is_only = False  # 是否业主 (家庭为单位) 在京唯一住房
    house.area = 120.0  # 房屋面积 (节点: 90, 140)
    house.building_year = 2000  # 建筑年代
    house.building_structure = "steel"  # 建筑结构: "steel": 钢混; "brick": 砖混
    house.position = 5  # 位置: 5: 5环内; 6: 5-6环; 7: 6环外
    house.monthly_rent = 0.9  # 估计月租金 (如自住设为0)
    house.cal_plans()
