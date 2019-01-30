from __future__ import print_function, absolute_import, unicode_literals
from datetime import datetime
import numpy as np
import math
from gm.api import *
import sys
from sklearn import svm
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas import DataFrame


# 计算 x1
# @para ： yes_open_price_day ：昨日开盘价
# @para ：close_price_k ：今日5分钟k线收盘价
def calculateX1(yes_open_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x1.append(yes_open_price_day / close_price_k[i] - 1)


# 计算 x2
# @para ： yes_close_price_day ：昨日收盘价
# @para ：close_price_k ：今日5分钟k线收盘价
def calculateX2(yes_close_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x2.append(yes_close_price_day / close_price_k[i] - 1)


# 计算 x3
# @para ： yes_high_price_day ：昨最高价
# @para ：close_price_k ：今日5分钟k线收盘价
def calculateX3(yes_high_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x3.append(yes_high_price_day / close_price_k[i] - 1)


# 计算 x4
# @para ： yes_low_price_day ：昨日最低价
# @para ：close_price_k ：今日5分钟k线收盘价
def calculateX4(yes_low_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x4.append(yes_low_price_day / close_price_k[i] - 1)


# 计算 x5
# @para ： yes_volume ：昨日成交量
# @para ：volume_k ：今日5分钟k线成交量
def calculateX5(yes_volume, volume_k):
    for i in range(0, len(volume_k)):
        x5.append(float(volume_k[i]) / yes_volume - 1)


# 计算 x6
# para ： yesterday_close_price_k ：昨日5分钟k线数据
# para ： close_price_k ：今日5分钟k线成交量
def calculateX6(yesterday_close_price_k, close_price_k):
    # 计算昨日波动率
    temp_sum = 0
    for i in range(0, len(yesterday_close_price_k)):
        temp_sum = temp_sum + yesterday_close_price_k[i]
    temp_sum = temp_sum / len(yesterday_close_price_k)  # 昨日平均值
    biaozhun_sum = 0
    for i in range(0, len(yesterday_close_price_k)):
        biaozhun_sum = biaozhun_sum + (yesterday_close_price_k[i] - temp_sum) * (
                yesterday_close_price_k[i] - temp_sum)
    biaozhun_sum = biaozhun_sum / len(yesterday_close_price_k)
    biaozhun_sum = math.sqrt(biaozhun_sum)  # 昨日标准差

    # 计算最新波动率
    for i in range(0, len(close_price_k)):
        temp_sum = 0
        for j in range(0, i + 1):
            temp_sum = temp_sum + close_price_k[j]
        temp_sum = temp_sum / (i + 1)
        biaozhun_sum2 = 0
        for j in range(0, i + 1):
            biaozhun_sum2 = biaozhun_sum2 + (close_price_k[j] - temp_sum) * (close_price_k[j] - temp_sum)
        biaozhun_sum2 = biaozhun_sum2 / (i + 1)
        biaozhun_sum2 = math.sqrt(biaozhun_sum2)
        # print(biaozhun_sum2)
        x6.append((biaozhun_sum2 / biaozhun_sum) - 1)


# 计算 x7
# @para ： today_open_price_day ：今日开盘价
# @para ：volume_k ：今日5分钟k线成交量
def calculateX7(today_open_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x7.append(today_open_price_day / close_price_k[i] - 1)


# 计算 x8
# @para ： high_price_k ：今日5分钟k线最高价
# @para ：volume_k ：今日5分钟k线成交量
def calculateX8(high_price_k, close_price_k):
    for i in range(0, len(close_price_k)):
        temp_max = high_price_k[0]
        for j in range(0, i + 1):
            if high_price_k[j] > temp_max:
                temp_max = high_price_k[j]
        x8.append(temp_max / close_price_k[i] - 1)


# 计算 x9
# @para ： low_price_k ：今日5分钟k线最低价
# @para ：volume_k ：今日5分钟k线成交量
def calculateX9(low_price_k, close_price_k):
    for i in range(0, len(close_price_k)):
        temp_min = low_price_k[0]
        for j in range(0, i + 1):
            if low_price_k[j] < temp_min:
                temp_min = low_price_k[j]
        x9.append(temp_min / close_price_k[i] - 1)


# 计算Y
def calculateY(today_close_price_day, close_price_k):
    # 计算对应的标签
    for i in range(0, len(close_price_k)):
        if close_price_k[i] < today_close_price_day:
            y_all.append(1)
        else:
            y_all.append(-1)


# 计算X
# para ：dayNum ：训练天数(第一天到第dayNum天)
# para ：k_bar_data ： 每日5分钟k线数据
def calculateX(dayNum, k_bar_data):

    # 获取昨日天数据
    # 获取数据,注意第一个数据的昨天数据没有，所以应该从第二个使用 每个_day是对应的昨日数据
    # (数组内存的是每一天的昨日的日数据)
    open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift()  # 获取昨日开盘价
    close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).first().shift()  # 获取昨日收盘价
    high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()  # 获取昨日最高价
    low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()  # 获取昨日最低价
    volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()  # 获取昨日成交量

    # 如果指定日期比所有天数还大 返回错误
    if dayNum > len(day_date_list):
        return "arrayOutOfIndex"
    form_date = day_date_list[0]  # 昨日日期
    # 从第一天到指定天数
    print("开始训练！");
    for date in day_date_list[1:dayNum]:
        print("today:" + date)  # 输出今日日期

        # 今日k线数据
        k_bar = k_bar_data[k_bar_data["date"] == date].reset_index(drop=True)  # 获取当天k线bar数据
        open_price_k = k_bar["open"]  # 获取k线开盘价
        close_price_k = k_bar["close"]  # 获取k线收盘价
        high_price_k = k_bar["high"]  # 获取k线最高价
        low_price_k = k_bar["low"]  # 获取k线最高价
        volume_k = k_bar["volume"]  # 获取k线成交量

        # 昨日k线数据
        yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # 获取昨天k线bar数据
        yesterday_close_price_k = yesterday_k_bar["close"]  # 获取昨日k线收盘价

        # 昨日天数据
        yes_open_price_day = open_price_day[date]  # 获取昨日开盘价
        yes_close_price_day = close_price_day[date]  # 获取昨日收盘价
        yes_high_price_day = high_price_day[date]  # 获取昨日最高价
        yes_low_price_day = low_price_day[date]  # 获取昨日最低价
        yes_volume = volume_day[date]  # 获取昨日成交量

        # 今日数据
        today_open_price_day = open_price_k[0]  # 今日开盘价
        today_close_price_day = close_price_k[len(close_price_k) - 1]  # 今日收盘价

        # 计算x1 x2 x3 x4 x5 x7 x8 x9
        calculateX1(yes_open_price_day, close_price_k)
        calculateX2(yes_close_price_day, close_price_k)
        calculateX3(yes_high_price_day, close_price_k)
        calculateX4(yes_low_price_day, close_price_k)
        calculateX6(yesterday_close_price_k, close_price_k)
        calculateX5(yes_volume, volume_k)
        calculateX7(today_open_price_day, close_price_k)
        calculateX8(high_price_k, close_price_k)
        calculateX9(low_price_k, close_price_k)

        calculateY(today_close_price_day, close_price_k)

    for i in range(0, len(x1)):
        feature = [x1[i], x2[i], x3[i], x4[i], x5[i], x6[i], x7[i], x8[i], x9[i]]
        x_all.append(feature)

    print("计算完成！")


# 回测函数
# para ：dayNum ：回测第dayNum天到最后
# para ：k_bar_data ：每日5分钟k线数据
def traceBackTest(dayNum, k_bar_data):

    # 获取昨日天数据
    # 获取数据,注意第一个数据的昨天数据没有，所以应该从第二个使用 每个_day是对应的昨日数据
    # (数组内存的是每一天的昨日的日数据)
    open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift()  # 获取昨日开盘价
    close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).first().shift()  # 获取昨日收盘价
    high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()  # 获取昨日最高价
    low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()  # 获取昨日最低价
    volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()  # 获取昨日成交量

    # 如果指定日期比所有天数还大 返回错误
    if dayNum > len(day_date_list):
        return "arrayOutOfIndex"
    form_date = day_date_list[dayNum]  # 昨日日期
    # 从dayNum到最后
    print("开始回测！");
    for date in day_date_list[dayNum:]:
        print("today:" + date)  # 输出今日日期

        # 今日k线数据
        k_bar = k_bar_data[k_bar_data["date"] == date].reset_index(drop=True)  # 获取当天k线bar数据
        open_price_k = k_bar["open"]  # 获取k线开盘价
        close_price_k = k_bar["close"]  # 获取k线收盘价
        high_price_k = k_bar["high"]  # 获取k线最高价
        low_price_k = k_bar["low"]  # 获取k线最高价
        volume_k = k_bar["volume"]  # 获取k线成交量

        # 昨日k线数据
        yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # 获取昨天k线bar数据
        yesterday_close_price_k = yesterday_k_bar["close"]  # 获取昨日k线收盘价

        # 昨日天数据
        yes_open_price_day = open_price_day[date]  # 获取昨日开盘价
        yes_close_price_day = close_price_day[date]  # 获取昨日收盘价
        yes_high_price_day = high_price_day[date]  # 获取昨日最高价
        yes_low_price_day = low_price_day[date]  # 获取昨日最低价
        yes_volume = volume_day[date]  # 获取昨日成交量

        # 今日数据
        today_open_price_day = open_price_k[0]  # 今日开盘价
        today_close_price_day = close_price_k[len(close_price_k) - 1]  # 今日收盘价

        # 计算x1 x2 x3 x4 x5 x7 x8 x9
        calculateX1(yes_open_price_day, close_price_k)
        calculateX2(yes_close_price_day, close_price_k)
        calculateX3(yes_high_price_day, close_price_k)
        calculateX4(yes_low_price_day, close_price_k)
        calculateX6(yesterday_close_price_k, close_price_k)
        calculateX5(yes_volume, volume_k)
        calculateX7(today_open_price_day, close_price_k)
        calculateX8(high_price_k, close_price_k)
        calculateX9(low_price_k, close_price_k)

        # 定义交易记录所需要内容
        #
        fill_price = []  # 成交价格（其实就是每k线收盘价）
        comission = []  # 手续费
        tv = []  # 成交额
        busy_type = []  # 成交类型（买还是卖）
        position_s = []  # 金钱流水
        profit = []  # k线利润
        isRight = []  # 预测正确与否
        temp_index = 0  # 临时下标，属于一个临时变量
        position = 0  # 持仓量
        predictions = []  # 预测的结果

        # 交易设置
        per_trade_cap = 1000  # 每次交易市值
        commision_ratio = 0.00018  # 手续费率
        tax_ratio = 0.001  # 印花税率
        days_trade_record = DataFrame()  # 多日交易记录汇总表

        # 对当日除最后一根k线外 进行预测买卖
        for i in range(len(x1) - len(open_price_k), len(x1) - 1):
            x_test = []
            feature = [x1[i], x2[i], x3[i], x4[i], x5[i], x6[i], x7[i], x8[i], x9[i]]  # 获取特征
            x_test.append(feature)
            prediction = clf.predict(x_test)[0]  # 进行预测
            x_test[:] = []  # 清空x_test
            predictions.append(prediction)  # 加入所有预测结果中
            per_trade_volume = (per_trade_cap / today_open_price_day).round(-2).astype(
                int)  # 用每次交易市值和每天的开盘价计算出每次交易的股数

            # 如果预测涨了 应该去买
            if prediction == 1:
                buy_price = close_price_k[temp_index]  # 记录买价
                # 如果当前k线收盘价大于今日收盘价，说明预测错误
                if close_price_k[temp_index] > close_price_k[len(close_price_k) - 1]:
                    isRight.append(-1)
                # 如果当前k线收盘价小于等于今日收盘价，说明预测正确
                if close_price_k[temp_index] <= close_price_k[len(close_price_k) - 1]:
                    isRight.append(1)
                temp_index = temp_index + 1
                fill_price.append(buy_price)  # 记录成交价
                tv.append(buy_price * per_trade_volume)  # 本次成交额
                comission.append(buy_price * commision_ratio * per_trade_volume)  # 记录交易费用
                position = position + per_trade_volume  # 记录持仓量
                position_s.append(position)  # 将持仓加入记录
                busy_type.append("buy")  # 记录买卖类型
                temp_profit = -buy_price * commision_ratio * per_trade_volume - buy_price * per_trade_volume  # 记录本次花去的钱
                profit.append(temp_profit)
            else:  # 预测跌了 卖
                sell_price = close_price_k[temp_index]  # 记录卖价
                # 如果当前k线收盘价大于等于今日收盘价，说明预测正确
                if close_price_k[temp_index] >= close_price_k[len(close_price_k) - 1]:
                    isRight.append(1)
                # 如果当前k线收盘价小于今日收盘价，说明预测错误
                if close_price_k[temp_index] < close_price_k[len(close_price_k) - 1]:
                    isRight.append(-1)
                temp_index = temp_index + 1
                fill_price.append(sell_price)  # 记录成交价
                tv.append(sell_price * per_trade_volume)  # 记录成交额
                comission.append(sell_price * per_trade_volume * (commision_ratio + tax_ratio))  # 记录交易费用
                position = position - per_trade_volume  # 记录持仓量
                position_s.append(position)  # 将持仓加入记录
                busy_type.append("sell")  # 记录买卖类型
                temp_profit = -sell_price * per_trade_volume * (
                        commision_ratio + tax_ratio) + sell_price * per_trade_volume  # 记录本次花去的钱
                profit.append(temp_profit)

        # 日末平仓
        profit_end = 0
        busy_type.append("close")
        fill_price.append(close_price_k[len(close_price_k) - 1])
        predictions.append(0)

        for i in range(0, len(fill_price)):
            if busy_type[i] == "buy":
                profit_end = profit_end - tv[i] - comission[i]
            if busy_type[i] == "sell":
                profit_end = profit_end + tv[i] - comission[i]
        # 日末还有持仓 以日未收盘价卖出平仓
        if position > 0:
            close_end = close_price_k[len(close_price_k) - 1]
            comission_end = close_end * position * (commision_ratio + tax_ratio)
            comission.append(comission_end)
            tv.append(close_end * position)
            profit_end = close_end * position - comission_end
            profit.append(profit_end)
        if position < 0:
            close_end = close_price_k[len(close_price_k) - 1]
            comission_end = close_end * (0 - position) * commision_ratio
            comission.append(comission_end)
            tv.append(close_end * (0 - position))
            profit_end = - close_end * (0 - position) - comission_end
            profit.append(profit_end)
        position_s.append(0)
        countIsRight = 0.0
        countIsError = 0.0
        for i in range(len(isRight) - len(open_price_k), len(isRight) - 1):
            if isRight[i] == 1:
                countIsRight = countIsRight + 1
            if isRight[i] == -1:
                countIsError = countIsError + 1
        isRight.append(countIsRight / (countIsRight + countIsError))
        pn_profit = []  # 收益，k线内累计收益

        for i in range(0, len(profit)):

            temp_sum = 0
            for j in range(0, i + 1):
                temp_sum = temp_sum + profit[j]
            pn_profit.append(temp_sum)

        # 组织交易记录表
        daily_trade_record = {
            "symbol": k_bar["symbol"],
            "date": k_bar["date"],
            "time": k_bar["eob"].apply(lambda x: x[11:]),
            "busy_type": busy_type,
            "fill_price": fill_price,
            "comission": comission,
            "tv": tv,
            "position_s": position_s,
            "profit": profit,
            "pn_profit": pn_profit,
            "isRight": isRight,
            "predictions": predictions
        }
        columns = ["symbol", "date", "time", "busy_type", "fill_price", "comission", "tv", "position_s",
                   "profit", "pn_profit", "isRight", "predictions"]
        daily_trade_record = DataFrame(daily_trade_record, columns=columns)
        days_trade_record = pd.concat([days_trade_record, daily_trade_record], axis=0)  # 将当日交易记录加入多日交易记录

    out_file_path = "E:/test_data/result/" + symbol + "_trade_record.csv"
    days_trade_record.to_csv(out_file_path, index=None)  # 输出交易记录


if __name__ == '__main__':
    begin_time = datetime.now()  # 记录初始时间

    symbols = pd.read_csv("E:/test_data/choose.csv")  # 获取股票代号
    data_path = "E:/test_data/data/"  # 设置bar数据路径

    # 遍历所有股票
    #
    for symbol in symbols:

        file_path = data_path + symbol + ".csv"  # 设置读取文件路径
        if (not os.path.exists("E:/test_data/result/" + symbol)):  # 每只股票创建一个文件夹保存记录，若不存在，创建
            os.mkdir("E:/test_data/result/" + symbol)

        #   获取日期
        #
        k_bar_data = pd.read_csv(file_path)  # 读取bar数据
        date_list = k_bar_data["bob"].apply(lambda x: x[:10].replace("-", ""))  # 获得k线日期
        k_bar_data.insert(1, "date", date_list)  # 将获得的日期插入dataframe
        day_date_list = k_bar_data["date"].groupby(k_bar_data["date"]).first()  # 获取每日日期

        # 数据处理，计算x_train,y_train
        #
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

        # SVM
        clf = svm.SVC(C=0.2, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                      tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                      decision_function_shape='ovr', random_state=None)
        dayNum = math.floor(len(day_date_list) * 0.8)
        calculateX(dayNum, k_bar_data)
        print(len(day_date_list))
        print(len(x_all))
        print(len(y_all))
        clf.fit(x_all, y_all)
        print('训练完成!')
        traceBackTest(dayNum, k_bar_data)
        print("回测完成！")
