from __future__ import print_function, absolute_import, unicode_literals
from datetime import datetime
import math
from sklearn import svm
import pandas as pd
import os
from pandas import DataFrame
import matplotlib.pyplot as plt
import my_calculate


# 计算 x
# @param ：begin_day ：开始日期
# @param ：end_day ：结束日期
def calculate_x(begin_day, end_day):
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
    for now_day in day_date_list[begin_day:end_day]:
        # 输出今日日期
        print("today:" + now_day)

        # 获取当天k线bar数据
        k_bar = k_bar_data[k_bar_data["date"] == now_day].reset_index(drop=True)
        open_price_k = k_bar["open"]  # 获取k线开盘价
        close_price_k = k_bar["close"]  # 获取k线收盘价
        high_price_k = k_bar["high"]  # 获取k线最高价
        low_price_k = k_bar["low"]  # 获取k线最高价
        volume_k = k_bar["volume"]  # 获取k线成交量
        time_k = k_bar["time"]  # 获取k线时间

        # 昨日k线数据
        yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # 获取昨天k线bar数据
        yesterday_close_price_k = yesterday_k_bar["close"]  # 获取昨日k线收盘价

        # 昨日天数据
        yesterday_open_price_day = open_price_day[now_day]  # 获取昨日开盘价
        yesterday_close_price_day = close_price_day[now_day]  # 获取昨日收盘价
        yesterday_high_price_day = high_price_day[now_day]  # 获取昨日最高价
        yesterday_low_price_day = low_price_day[now_day]  # 获取昨日最低价
        yesterday_volume = volume_day[now_day]  # 获取昨日成交量

        # 今日天数据
        today_open_price_day = open_price_k[0]  # 今日开盘价
        today_close_price_day = close_price_k[len(close_price_k) - 1]  # 今日收盘价

        # 对交易时间前一条k线进行训练 此时暂定交易时间前一条k线为 trade_time = "10:25:00"
        for i in range(len(close_price_k)):
            print("now_time:" + time_k[i])
            # 如果训练日当前时间 等于 交易时间上一条k线时间 带入数据进行计算
            if time_k[i] == trade_time:
                x1.append(my_calculate.calculate_x1(yesterday_open_price_day, close_price_k[i]))
                x2.append(my_calculate.calculate_x2(yesterday_close_price_day, close_price_k[i]))
                x3.append(my_calculate.calculate_x3(yesterday_high_price_day, close_price_k[i]))
                x4.append(my_calculate.calculate_x4(yesterday_low_price_day, close_price_k[i]))
                now_volume = 0  # 最新成交量
                for j in range(0, i):
                    now_volume = now_volume + volume_k[j]
                now_volume2 = my_calculate.calculate_new_volume(now_volume, len(close_price_k), i + 1)  # 计算加权后的最新成交量
                x5.append(my_calculate.calculate_x5(yesterday_volume, now_volume2))
                yes_bo_dong_lv = my_calculate.calculate_yes_bo_dong_lv(yesterday_close_price_k)  # 计算昨日波动率
                new_bo_dong_lv = my_calculate.calculate_new_bo_dong_lv(close_price_k[0:i + 1], len(close_price_k),
                                                                       i + 1)  # 计算最新波动率
                x6.append(my_calculate.calculate_x6(yes_bo_dong_lv, new_bo_dong_lv))
                x7.append(my_calculate.calculate_x7(today_open_price_day, close_price_k[i]))
                new_max = max(high_price_k[0:i + 1])  # 计算最新最高价
                x8.append(my_calculate.calculate_x8(new_max, close_price_k[i]))
                new_min = min(low_price_k[0:i + 1])  # 计算最新最低价
                x9.append(my_calculate.calculate_x9(new_min, close_price_k[i]))
                length = len(x1) - 1
                feature = [x1[length], x2[length], x3[length], x4[length], x5[length], x6[length], x7[length],
                           x8[length], x9[length]]
                print(feature)
                x_all.append(feature)
                y_all.append(my_calculate.calculate_y(today_close_price_day, close_price_k[i]))
                break
    print("计算完成")


# 清空数组 x1 - x9 和 y_all 、 x_all
def clear_list():
    x1.clear()
    x2.clear()
    x3.clear()
    x4.clear()
    x5.clear()
    x6.clear()
    x7.clear()
    x8.clear()
    x9.clear()
    x_all.clear()
    y_all.clear()


# 模拟买
# 每次模拟买入1000股
# @param ： now_day ： 当前日
def buy(now_day):
    # 获取当前日k线数据用于模拟交易
    k_bar = k_bar_data[k_bar_data["date"] == now_day].reset_index(drop=True)
    close_price_k = k_bar["close"]  # 获取k线收盘价
    time_k = k_bar["time"]  # 获取k线时间
    flag_begin_buy = 0  # 当前是否可以开始交易
    now_volume = 0  # 每一次交易数量
    now_price = []  # 每一次交易价格
    commission_ratio = 0.00018  # 手续费率
    tax_ratio = 0.001  # 印花税率
    commission_price = [] # 手续费
    buy_volume = 1000  # 每次买入股数
    ave_price = 0  # 平均买入价格
    buy_time = 0  # 买入次数
    profit = 0 # 当天利润
    flag = 0  # 标记是否连续涨
    for i in range(len(close_price_k)):
        # 如果当预定交易时间，则可以进行交易
        if time_k[i] == "10:30:00":
            now_volume = buy_volume  # 买入一定股数
            now_price.append(close_price_k[i])  # 记录买入价格
            ave_price = ave_price + close_price_k[i]  # 计算平均价格
            buy_time = buy_time + 1  # 买入次数+1
            commission_price.append(buy_volume*close_price_k[i]*commission_ratio)
            flag_begin_buy = 1  # 标记可以进行交易
            continue
        # 如果可以进行交易
        # (1) 如果之后直接涨了 高于现在手中平均价格 继续买入
        # (2) 如果涨了又跌了 但是此时价格大于平均价格 或者盈利达到百分一 止盈
        # (3) 如果直接跌破百分之三 直接止损卖出
        if flag_begin_buy == 1:
            # 如果下面的k线相对于底仓价格涨了 并且 相对于前一条k线还是涨的，那么买入
            if close_price_k[i] > now_price[0] and close_price_k[i] > close_price_k[i - 1]:
                now_volume = now_volume + buy_volume  # 继续买入一定股数
                now_price.append(close_price_k[i])  # 记录买入价格
                buy_time = buy_time + 1  # 买入次数+1
                commission_price.append(buy_volume*close_price_k[i]*commission_ratio)
                ave_price = sum(now_price) / buy_time  # 计算平均买入价格
            # 如果下面的k线相对于底仓价格涨了 并且 相对于前一条k线还是跌了的，那么卖出
            if close_price_k[i] > now_price[0] and close_price_k[i] < close_price_k[i - 1]:
                if (close_price_k[i] - ave_price) / ave_price > 0.008:
                    profit = (close_price_k[i] - ave_price)*sum(now_volume)*(1-commission_ratio-tax_ratio)




# 回测
# @param ：begin_day ：开始日期
# @param ：end_day ：结束日期
def trade_back_test(begin_day, end_day):
    calculate_x(begin_day, end_day)  # 获取每天结果（注意这里y_all 也得到了但是属于未来数据不能用）
    i = 0
    predictions = []
    for now_day in range(begin_day, end_day):
        # 预测买卖
        temp_test_x = [x_all[i]]
        # print(temp_test_x)
        prediction = clf.predict(temp_test_x)[0]  # 进行预测
        # print(prediction)
        predictions.append(prediction)
        # 如果预测涨 买进
        if prediction == 1:
            print("1")
        else:  # 如果预测跌 卖出
            print("1")
        i = i + 1


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
    # 设置交易时间 前一条k线
    trade_time = "10:25:00"

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
        clf = svm.SVC(C=0.8, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                      tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                      decision_function_shape='ovr', random_state=None)
        # 定义训练天数
        day_num = math.floor(len(day_date_list) * 0.8)
        calculate_x(1, day_num)
        print("开始训练！")
        clf.fit(x_all, y_all)
        print("训练结束！")
        # 将训练数据保存到 csv 文件
        train_frame = pd.DataFrame(
            {'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4, 'x5': x5, 'x6': x6, 'x7': x7, 'x8': x8, 'x9': x9, 'y': y_all})
        train_frame.to_csv("E:/test_data/result/" + symbol + "/train.csv", index=False, sep=',')

        # TODO
        # 将训练数据回代入svm 模型

        # 清空之前结果
        clear_list()

        print("开始回测！")
        trade_back_test(day_num, len(day_date_list))
        print("回测结束！")
        break
    print("谢谢！")
