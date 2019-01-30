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


# ���� x1
# @para �� yes_open_price_day �����տ��̼�
# @para ��close_price_k ������5����k�����̼�
def calculateX1(yes_open_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x1.append(yes_open_price_day / close_price_k[i] - 1)


# ���� x2
# @para �� yes_close_price_day ���������̼�
# @para ��close_price_k ������5����k�����̼�
def calculateX2(yes_close_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x2.append(yes_close_price_day / close_price_k[i] - 1)


# ���� x3
# @para �� yes_high_price_day ������߼�
# @para ��close_price_k ������5����k�����̼�
def calculateX3(yes_high_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x3.append(yes_high_price_day / close_price_k[i] - 1)


# ���� x4
# @para �� yes_low_price_day ��������ͼ�
# @para ��close_price_k ������5����k�����̼�
def calculateX4(yes_low_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x4.append(yes_low_price_day / close_price_k[i] - 1)


# ���� x5
# @para �� yes_volume �����ճɽ���
# @para ��volume_k ������5����k�߳ɽ���
def calculateX5(yes_volume, volume_k):
    for i in range(0, len(volume_k)):
        x5.append(float(volume_k[i]) / yes_volume - 1)


# ���� x6
# para �� yesterday_close_price_k ������5����k������
# para �� close_price_k ������5����k�߳ɽ���
def calculateX6(yesterday_close_price_k, close_price_k):
    # �������ղ�����
    temp_sum = 0
    for i in range(0, len(yesterday_close_price_k)):
        temp_sum = temp_sum + yesterday_close_price_k[i]
    temp_sum = temp_sum / len(yesterday_close_price_k)  # ����ƽ��ֵ
    biaozhun_sum = 0
    for i in range(0, len(yesterday_close_price_k)):
        biaozhun_sum = biaozhun_sum + (yesterday_close_price_k[i] - temp_sum) * (
                yesterday_close_price_k[i] - temp_sum)
    biaozhun_sum = biaozhun_sum / len(yesterday_close_price_k)
    biaozhun_sum = math.sqrt(biaozhun_sum)  # ���ձ�׼��

    # �������²�����
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


# ���� x7
# @para �� today_open_price_day �����տ��̼�
# @para ��volume_k ������5����k�߳ɽ���
def calculateX7(today_open_price_day, close_price_k):
    for i in range(0, len(close_price_k)):
        x7.append(today_open_price_day / close_price_k[i] - 1)


# ���� x8
# @para �� high_price_k ������5����k����߼�
# @para ��volume_k ������5����k�߳ɽ���
def calculateX8(high_price_k, close_price_k):
    for i in range(0, len(close_price_k)):
        temp_max = high_price_k[0]
        for j in range(0, i + 1):
            if high_price_k[j] > temp_max:
                temp_max = high_price_k[j]
        x8.append(temp_max / close_price_k[i] - 1)


# ���� x9
# @para �� low_price_k ������5����k����ͼ�
# @para ��volume_k ������5����k�߳ɽ���
def calculateX9(low_price_k, close_price_k):
    for i in range(0, len(close_price_k)):
        temp_min = low_price_k[0]
        for j in range(0, i + 1):
            if low_price_k[j] < temp_min:
                temp_min = low_price_k[j]
        x9.append(temp_min / close_price_k[i] - 1)


# ����Y
def calculateY(today_close_price_day, close_price_k):
    # �����Ӧ�ı�ǩ
    for i in range(0, len(close_price_k)):
        if close_price_k[i] < today_close_price_day:
            y_all.append(1)
        else:
            y_all.append(-1)


# ����X
# para ��dayNum ��ѵ������(��һ�쵽��dayNum��)
# para ��k_bar_data �� ÿ��5����k������
def calculateX(dayNum, k_bar_data):

    # ��ȡ����������
    # ��ȡ����,ע���һ�����ݵ���������û�У�����Ӧ�ôӵڶ���ʹ�� ÿ��_day�Ƕ�Ӧ����������
    # (�����ڴ����ÿһ������յ�������)
    open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift()  # ��ȡ���տ��̼�
    close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).first().shift()  # ��ȡ�������̼�
    high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()  # ��ȡ������߼�
    low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()  # ��ȡ������ͼ�
    volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()  # ��ȡ���ճɽ���

    # ���ָ�����ڱ������������� ���ش���
    if dayNum > len(day_date_list):
        return "arrayOutOfIndex"
    form_date = day_date_list[0]  # ��������
    # �ӵ�һ�쵽ָ������
    print("��ʼѵ����");
    for date in day_date_list[1:dayNum]:
        print("today:" + date)  # �����������

        # ����k������
        k_bar = k_bar_data[k_bar_data["date"] == date].reset_index(drop=True)  # ��ȡ����k��bar����
        open_price_k = k_bar["open"]  # ��ȡk�߿��̼�
        close_price_k = k_bar["close"]  # ��ȡk�����̼�
        high_price_k = k_bar["high"]  # ��ȡk����߼�
        low_price_k = k_bar["low"]  # ��ȡk����߼�
        volume_k = k_bar["volume"]  # ��ȡk�߳ɽ���

        # ����k������
        yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # ��ȡ����k��bar����
        yesterday_close_price_k = yesterday_k_bar["close"]  # ��ȡ����k�����̼�

        # ����������
        yes_open_price_day = open_price_day[date]  # ��ȡ���տ��̼�
        yes_close_price_day = close_price_day[date]  # ��ȡ�������̼�
        yes_high_price_day = high_price_day[date]  # ��ȡ������߼�
        yes_low_price_day = low_price_day[date]  # ��ȡ������ͼ�
        yes_volume = volume_day[date]  # ��ȡ���ճɽ���

        # ��������
        today_open_price_day = open_price_k[0]  # ���տ��̼�
        today_close_price_day = close_price_k[len(close_price_k) - 1]  # �������̼�

        # ����x1 x2 x3 x4 x5 x7 x8 x9
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

    print("������ɣ�")


# �ز⺯��
# para ��dayNum ���ز��dayNum�쵽���
# para ��k_bar_data ��ÿ��5����k������
def traceBackTest(dayNum, k_bar_data):

    # ��ȡ����������
    # ��ȡ����,ע���һ�����ݵ���������û�У�����Ӧ�ôӵڶ���ʹ�� ÿ��_day�Ƕ�Ӧ����������
    # (�����ڴ����ÿһ������յ�������)
    open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift()  # ��ȡ���տ��̼�
    close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).first().shift()  # ��ȡ�������̼�
    high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()  # ��ȡ������߼�
    low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()  # ��ȡ������ͼ�
    volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()  # ��ȡ���ճɽ���

    # ���ָ�����ڱ������������� ���ش���
    if dayNum > len(day_date_list):
        return "arrayOutOfIndex"
    form_date = day_date_list[dayNum]  # ��������
    # ��dayNum�����
    print("��ʼ�ز⣡");
    for date in day_date_list[dayNum:]:
        print("today:" + date)  # �����������

        # ����k������
        k_bar = k_bar_data[k_bar_data["date"] == date].reset_index(drop=True)  # ��ȡ����k��bar����
        open_price_k = k_bar["open"]  # ��ȡk�߿��̼�
        close_price_k = k_bar["close"]  # ��ȡk�����̼�
        high_price_k = k_bar["high"]  # ��ȡk����߼�
        low_price_k = k_bar["low"]  # ��ȡk����߼�
        volume_k = k_bar["volume"]  # ��ȡk�߳ɽ���

        # ����k������
        yesterday_k_bar = k_bar_data[k_bar_data["date"] == form_date].reset_index(drop=True)  # ��ȡ����k��bar����
        yesterday_close_price_k = yesterday_k_bar["close"]  # ��ȡ����k�����̼�

        # ����������
        yes_open_price_day = open_price_day[date]  # ��ȡ���տ��̼�
        yes_close_price_day = close_price_day[date]  # ��ȡ�������̼�
        yes_high_price_day = high_price_day[date]  # ��ȡ������߼�
        yes_low_price_day = low_price_day[date]  # ��ȡ������ͼ�
        yes_volume = volume_day[date]  # ��ȡ���ճɽ���

        # ��������
        today_open_price_day = open_price_k[0]  # ���տ��̼�
        today_close_price_day = close_price_k[len(close_price_k) - 1]  # �������̼�

        # ����x1 x2 x3 x4 x5 x7 x8 x9
        calculateX1(yes_open_price_day, close_price_k)
        calculateX2(yes_close_price_day, close_price_k)
        calculateX3(yes_high_price_day, close_price_k)
        calculateX4(yes_low_price_day, close_price_k)
        calculateX6(yesterday_close_price_k, close_price_k)
        calculateX5(yes_volume, volume_k)
        calculateX7(today_open_price_day, close_price_k)
        calculateX8(high_price_k, close_price_k)
        calculateX9(low_price_k, close_price_k)

        # ���彻�׼�¼����Ҫ����
        #
        fill_price = []  # �ɽ��۸���ʵ����ÿk�����̼ۣ�
        comission = []  # ������
        tv = []  # �ɽ���
        busy_type = []  # �ɽ����ͣ���������
        position_s = []  # ��Ǯ��ˮ
        profit = []  # k������
        isRight = []  # Ԥ����ȷ���
        temp_index = 0  # ��ʱ�±꣬����һ����ʱ����
        position = 0  # �ֲ���
        predictions = []  # Ԥ��Ľ��

        # ��������
        per_trade_cap = 1000  # ÿ�ν�����ֵ
        commision_ratio = 0.00018  # ��������
        tax_ratio = 0.001  # ӡ��˰��
        days_trade_record = DataFrame()  # ���ս��׼�¼���ܱ�

        # �Ե��ճ����һ��k���� ����Ԥ������
        for i in range(len(x1) - len(open_price_k), len(x1) - 1):
            x_test = []
            feature = [x1[i], x2[i], x3[i], x4[i], x5[i], x6[i], x7[i], x8[i], x9[i]]  # ��ȡ����
            x_test.append(feature)
            prediction = clf.predict(x_test)[0]  # ����Ԥ��
            x_test[:] = []  # ���x_test
            predictions.append(prediction)  # ��������Ԥ������
            per_trade_volume = (per_trade_cap / today_open_price_day).round(-2).astype(
                int)  # ��ÿ�ν�����ֵ��ÿ��Ŀ��̼ۼ����ÿ�ν��׵Ĺ���

            # ���Ԥ������ Ӧ��ȥ��
            if prediction == 1:
                buy_price = close_price_k[temp_index]  # ��¼���
                # �����ǰk�����̼۴��ڽ������̼ۣ�˵��Ԥ�����
                if close_price_k[temp_index] > close_price_k[len(close_price_k) - 1]:
                    isRight.append(-1)
                # �����ǰk�����̼�С�ڵ��ڽ������̼ۣ�˵��Ԥ����ȷ
                if close_price_k[temp_index] <= close_price_k[len(close_price_k) - 1]:
                    isRight.append(1)
                temp_index = temp_index + 1
                fill_price.append(buy_price)  # ��¼�ɽ���
                tv.append(buy_price * per_trade_volume)  # ���γɽ���
                comission.append(buy_price * commision_ratio * per_trade_volume)  # ��¼���׷���
                position = position + per_trade_volume  # ��¼�ֲ���
                position_s.append(position)  # ���ֲּ����¼
                busy_type.append("buy")  # ��¼��������
                temp_profit = -buy_price * commision_ratio * per_trade_volume - buy_price * per_trade_volume  # ��¼���λ�ȥ��Ǯ
                profit.append(temp_profit)
            else:  # Ԥ����� ��
                sell_price = close_price_k[temp_index]  # ��¼����
                # �����ǰk�����̼۴��ڵ��ڽ������̼ۣ�˵��Ԥ����ȷ
                if close_price_k[temp_index] >= close_price_k[len(close_price_k) - 1]:
                    isRight.append(1)
                # �����ǰk�����̼�С�ڽ������̼ۣ�˵��Ԥ�����
                if close_price_k[temp_index] < close_price_k[len(close_price_k) - 1]:
                    isRight.append(-1)
                temp_index = temp_index + 1
                fill_price.append(sell_price)  # ��¼�ɽ���
                tv.append(sell_price * per_trade_volume)  # ��¼�ɽ���
                comission.append(sell_price * per_trade_volume * (commision_ratio + tax_ratio))  # ��¼���׷���
                position = position - per_trade_volume  # ��¼�ֲ���
                position_s.append(position)  # ���ֲּ����¼
                busy_type.append("sell")  # ��¼��������
                temp_profit = -sell_price * per_trade_volume * (
                        commision_ratio + tax_ratio) + sell_price * per_trade_volume  # ��¼���λ�ȥ��Ǯ
                profit.append(temp_profit)

        # ��ĩƽ��
        profit_end = 0
        busy_type.append("close")
        fill_price.append(close_price_k[len(close_price_k) - 1])
        predictions.append(0)

        for i in range(0, len(fill_price)):
            if busy_type[i] == "buy":
                profit_end = profit_end - tv[i] - comission[i]
            if busy_type[i] == "sell":
                profit_end = profit_end + tv[i] - comission[i]
        # ��ĩ���гֲ� ����δ���̼�����ƽ��
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
        pn_profit = []  # ���棬k�����ۼ�����

        for i in range(0, len(profit)):

            temp_sum = 0
            for j in range(0, i + 1):
                temp_sum = temp_sum + profit[j]
            pn_profit.append(temp_sum)

        # ��֯���׼�¼��
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
        days_trade_record = pd.concat([days_trade_record, daily_trade_record], axis=0)  # �����ս��׼�¼������ս��׼�¼

    out_file_path = "E:/test_data/result/" + symbol + "_trade_record.csv"
    days_trade_record.to_csv(out_file_path, index=None)  # ������׼�¼


if __name__ == '__main__':
    begin_time = datetime.now()  # ��¼��ʼʱ��

    symbols = pd.read_csv("E:/test_data/choose.csv")  # ��ȡ��Ʊ����
    data_path = "E:/test_data/data/"  # ����bar����·��

    # �������й�Ʊ
    #
    for symbol in symbols:

        file_path = data_path + symbol + ".csv"  # ���ö�ȡ�ļ�·��
        if (not os.path.exists("E:/test_data/result/" + symbol)):  # ÿֻ��Ʊ����һ���ļ��б����¼���������ڣ�����
            os.mkdir("E:/test_data/result/" + symbol)

        #   ��ȡ����
        #
        k_bar_data = pd.read_csv(file_path)  # ��ȡbar����
        date_list = k_bar_data["bob"].apply(lambda x: x[:10].replace("-", ""))  # ���k������
        k_bar_data.insert(1, "date", date_list)  # ����õ����ڲ���dataframe
        day_date_list = k_bar_data["date"].groupby(k_bar_data["date"]).first()  # ��ȡÿ������

        # ���ݴ�������x_train,y_train
        #
        # �������ݽṹ
        x1 = []  # ���տ��̼�/�������̼�-1
        x2 = []  # �������̼�/�������̼�-1
        x3 = []  # ������߼�/�������̼�-1
        x4 = []  # ������ͼ�/�������̼�-1
        x5 = []  # ���³ɽ���/���ճɽ���-1
        x6 = []  # ���²�����/���ղ�����-1
        x7 = []  # ���տ��̼�/�������̼�-1
        x8 = []  # ������߼�/�������̼�-1
        x9 = []  # ������ͼ�/�������̼�-1

        x_all = []  # ��������x
        y_all = []  # ��������y

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
        print('ѵ�����!')
        traceBackTest(dayNum, k_bar_data)
        print("�ز���ɣ�")
