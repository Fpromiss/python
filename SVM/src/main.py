from __future__ import print_function, absolute_import, unicode_literals
from datetime import datetime
import math
from sklearn import svm
import pandas as pd
import os
from pandas import DataFrame
import matplotlib.pyplot as plt
import src.calculate as calculate_x


# 计算 x
def calculate_x():
    # 获取昨日天数据
    # 获取数据,注意第一个数据的昨天数据没有，所以应该从第二个使用 每个_day是对应的昨日数据
    # (数组内存的是每一天的昨日的日数据)
    open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift()  # 获取昨日开盘价
    close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).last().shift()  # 获取昨日收盘价
    high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()  # 获取昨日最高价
    low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()  # 获取昨日最低价
    volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()  # 获取昨日成交量

    # 如果指定日期比所有天数还大 返回错误
    if day_num > len(day_date_list):
        return "arrayOutOfIndex"

    form_date = day_date_list[0]  # 昨日日期
    # 从第一天到指定天数
    print("开始训练！")
    for now_day in day_date_list[1:day_num]:
        # 输出今日日期
        print("today:" + now_day)

        # 获取当天k线bar数据
        k_bar = k_bar_data[k_bar_data["date"] == now_day].reset_index(drop=True)
        open_price_k = k_bar["open"]  # 获取k线开盘价
        close_price_k = k_bar["close"]  # 获取k线收盘价
        high_price_k = k_bar["high"]  # 获取k线最高价
        low_price_k = k_bar["low"]  # 获取k线最高价
        volume_k = k_bar["volume"]  # 获取k线成交量
        print("hello" + str(open_price_k))

        # # 昨日k线数据
        # yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # 获取昨天k线bar数据
        # yesterday_close_price_k = yesterday_k_bar["close"]  # 获取昨日k线收盘价
        # yesterday_open_price_day = open_price_day[now_day]  # 获取昨日开盘价
        # yesterday_close_price_day = close_price_day[now_day]  # 获取昨日收盘价
        # yesterday_high_price_day = high_price_day[now_day]  # 获取昨日最高价
        # yesterday_low_price_day = low_price_day[now_day]  # 获取昨日最低价
        # yesterday_volume = volume_day[now_day]  # 获取昨日成交量
        #
        # # 今日数据
        # today_open_price_day = open_price_k[0]  # 今日开盘价
        # today_close_price_day = close_price_k[len(close_price_k) - 1]  # 今日收盘价
        #
        # # 计算x1 - x9
        # x1.append(calculate_x.calculate_x1(yesterday_open_price_day, ))






if __name__ == '__main__':
    # 定义数据结构
    x1 = []  # 昨日开盘价/最新收盘价-1
    x2 = []  # 昨日收盘价/最新收盘价-1
    x3 = []  # 昨日最高价/最新收盘价-1
    x4 = []  # 昨日最低价/最新收盘价-1
    x5 = []  # 最新成交量/昨日成交量-1
    x6 = []  # 最新波动率/昨日波动率-1
    x7 = []  # 今日开盘价/最新收盘价-1
    x8 = []  # 最新最高价/最新收盘价-1
    x9 = []  # 最新最低价/最新收盘价-1
    x_all = []  # 定义所有x
    y_all = []  # 定义所有y

    # 获取股票代号
    symbols = pd.read_csv("E:/test_data/choose.csv")
    symbolList = symbols["stock"]
    # 设置bar数据路径
    data_path = "E:/test_data/data/"

    print("begin:")
    # 遍历所有股票
    for symbol in symbolList:
        print("now_do:" + symbol)
        # 设置读取文件路径
        file_path = data_path + symbol + ".csv"

        # 每只股票创建一个文件夹保存记录，若不存在，创建
        if (not os.path.exists("E:/test_data/result/" + symbol)):
            os.mkdir("E:/test_data/result/" + symbol)

        #  获取日期
        # 读取bar数据
        k_bar_data = pd.read_csv(file_path)
        # 获得k线日期
        date_list = k_bar_data["bob"].apply(lambda x: x[:10].replace("-", ""))
        # 将获得的日期插入data frame
        k_bar_data.insert(1, "date", date_list)
        # 获取每日日期
        day_date_list = k_bar_data["date"].groupby(k_bar_data["date"]).first()
        # 获取k线时间
        time_list = k_bar_data["bob"].apply(lambda x: x[11:].replace("-", ""))
        # 将获得的时间插入data frame
        k_bar_data.insert(1, "time", time_list)
        # 获取每日时间
        day_time_list = k_bar_data["time"].groupby(k_bar_data["time"]).first()


        # SVM
        clf = svm.SVC(C=0.2, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                      tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                      decision_function_shape='ovr', random_state=None)
        # 定义训练天数
        day_num = math.floor(len(day_date_list) * 0.8)
        calculate_x()
