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


begin_time = datetime.now()#记录初始时间

data_path="E:/test_data"#设置bar数据路径
frequency = "300s"#设置数据粒度
symbol = "SZSE.002210"#设置股票symbol
record_path = symbol #记录输出路径
file_path=data_path+"/"+frequency+"/"+symbol+".csv"#设置读取文件路径

if(not os.path.exists(symbol)):#每只股票创建一个文件夹保存记录，若不存在，创建
    os.mkdir(symbol)
    
k_bar_data= pd.read_csv(file_path) # 读取bar数据
date_list = k_bar_data["bob"].apply(lambda x:x[:10].replace("-","")) # 获得k线日期
k_bar_data.insert(1,"date",date_list) #将获得的日期插入dataframe
print(date_list[0:10])
day_date_list = k_bar_data["date"].groupby(k_bar_data["date"]).first()#获取每日日期
print(day_date_list[0:10])


#获取数据,注意第一个数据的昨天数据没有，所以应该从第二个使用 每个_day是对应的昨日数据
open_price_day = k_bar_data["open"].groupby(k_bar_data["date"]).first().shift() #获取昨日开盘价
close_price_day = k_bar_data['close'].groupby(k_bar_data["date"]).first().shift()#获取昨日收盘价
high_price_day = k_bar_data["high"].groupby(k_bar_data["date"]).max().shift()#获取昨日最高价
low_price_day = k_bar_data["low"].groupby(k_bar_data["date"]).min().shift()#获取昨日最低价
volume_day = k_bar_data["volume"].groupby(k_bar_data["date"]).sum().shift()#获取昨日成交量



#数据处理，计算x_train,y_train
x1 = []#昨日开盘价/最新收盘价-1
x2 = []#昨日收盘价/最新收盘价-1
x3 = []#昨日最高价/最新收盘价-1
x4 = []#昨日最低价/最新收盘价-1
x5 = []#最新成交量/昨日成交量-1
x6 = []#最新波动率/昨日波动率-1
x7 = []#今日开盘价/最新收盘价-1
x8 = []#最新最高价/最新收盘价-1
x9 = []#最新最低价/最新收盘价-1

x_all = []
y_all = []
count = 0
test_flag = 0
form_date = "20160104"
clf = svm.SVC(C=0.5, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                        tol=0.001, cache_size=400, verbose=False, max_iter=-1,
                        decision_function_shape='ovr', random_state=None)
per_trade_cap = 1000 #每次交易市值
commision_ratio = 0.00018 # 手续费率
tax_ratio = 0.001 #印花税率
days_trade_record = DataFrame() #多日交易记录汇总表


for date in day_date_list[1:]:
    print("today:"+date) 
    count = count + 1
    #如果四百天样本 训练
    if count == 401:
        clf.fit(x_all,y_all)
        print('训练完成!')
    #大于四百天回测
    if count>401:
        test_flag=1
        
    #今日k线数据
    k_bar = k_bar_data[k_bar_data["date"]==date].reset_index(drop = True) #获取当天k线bar数据
    open_price_k = k_bar["open"] #获取k线开盘价
    close_price_k=k_bar["close"]#获取k线收盘价
    high_price_k = k_bar["high"]#获取k线最高价
    low_price_k = k_bar["low"]#获取k线最高价
    volume_k = k_bar["volume"]#获取k线成交量
    #print("今日k成交量")
    #print(volume_k[0:10])
    
    #昨日k线数据
    yesterday_k_bar = k_bar_data[k_bar_data["date"]==form_date].reset_index(drop = True) #获取昨天k线bar数据
    yesterday_close_price_k=yesterday_k_bar["close"]#获取昨日k线收盘价
    
    #昨日天数据
    yes_open_price_day = open_price_day[date]#获取昨日开盘价
    yes_close_price_day = close_price_day[date]#获取昨日收盘价
    yes_high_price_day =high_price_day[date]#获取昨日最高价
    yes_low_price_day = low_price_day[date]#获取昨日最低价
    yes_volume =volume_day[date]#获取昨日成交量
    #print(yes_open_price_day)
    today_open_price_day = open_price_k[0]#今日开盘价
    today_close_price_day = close_price_k[len(close_price_k)-1]#今日收盘价
    #print(today_close_price_day)
    #print(today_open_price_day)
    
    #print("昨日成交量")
    #print(yes_volume)
    
    #print(len(open_price_k))
    #计算x1 x2 x3 x4 x5 x7
    for i in range(0,len(open_price_k)):
        x1.append(yes_open_price_day/close_price_k[i]-1)
        x2.append(yes_close_price_day/close_price_k[i]-1)
        x3.append(yes_high_price_day/close_price_k[i]-1)
        x4.append(yes_low_price_day/close_price_k[i]-1)
        x5.append(float(volume_k[i])/yes_volume-1)
        x7.append(today_open_price_day/close_price_k[i]-1)
    #print(len(x1))
    
    #计算x8 x9
    for i in range(0,len(open_price_k)):
        temp_max = high_price_k[0]
        temp_min = low_price_k[0]
        for j in range(0,i+1):
            if high_price_k[j]>temp_max :
                temp_max = high_price_k[j]
            if low_price_k[j]<temp_min :
                temp_min = low_price_k[j]
        x8.append(temp_max/close_price_k[i]-1)
        x9.append(temp_min/close_price_k[i]-1)
        
    #计算x6
    #计算昨日波动率
    temp_sum = 0
    for i in range(0,len(yesterday_close_price_k)):
        temp_sum = temp_sum + yesterday_close_price_k[i]
    temp_sum = temp_sum / len(yesterday_close_price_k)
    biaozhun_sum = 0
    for i in range(0,len(yesterday_close_price_k)):
        biaozhun_sum = biaozhun_sum + (yesterday_close_price_k[i]-temp_sum)*(yesterday_close_price_k[i]-temp_sum)
    biaozhun_sum = biaozhun_sum / len(yesterday_close_price_k)
    biaozhun_sum = math.sqrt(biaozhun_sum)
    #print(biaozhun_sum)
    
    #计算最新波动率
    for i in range(0,len(close_price_k)):
        temp_sum = 0
        for j in range(0,i+1):
            temp_sum = temp_sum + close_price_k[j]
        temp_sum = temp_sum / (i+1)
        biaozhun_sum2 = 0
        for j in range(0,i+1):
            biaozhun_sum2 = biaozhun_sum2 + (close_price_k[j]-temp_sum)*(close_price_k[j]-temp_sum)
        biaozhun_sum2 = biaozhun_sum2 / (i+1)
        biaozhun_sum2 = math.sqrt(biaozhun_sum2)
        #print(biaozhun_sum2)
        x6.append((biaozhun_sum2/biaozhun_sum)-1)
          
    if test_flag==0:
        for i in range(0,len(close_price_k)-1):
            feature = [x1[i],x2[i],x3[i],x4[i],x5[i],x6[i],x7[i],x8[i],x9[i]]
            x_all.append(feature)
        #print(x_train[0:10])
        #print(len(x_train))
    
    for i in range(0,len(close_price_k)-1):
        if close_price_k[i]<today_close_price_day:
            y_all.append(1)
        else:
            y_all.append(-1)
    #print(len(y_train))
    
    form_date=date
    
    if test_flag==1:
        print("回测")
        x_test= []
        fill_price=[]
        comission=[]
        tv=[]
        busy_type=[]
        position_s=[]#金钱流水
        profit=[]#k线利润
        pnl=[]
        isRight=[]#正确与否
        temp_index = 0
        position = 0
        predictions=[]#预测
        for i in range(len(x1)-len(open_price_k),len(x1)-1):
            feature = [x1[i],x2[i],x3[i],x4[i],x5[i],x6[i],x7[i],x8[i],x9[i]]
            x_test.append(feature)
            prediction = clf.predict(x_test)[0]
            predictions.append(prediction)
            x_test=[]
            per_trade_volume = (per_trade_cap/today_open_price_day).round(-2).astype(int) #用每次交易市值和每天的开盘价计算出每次交易的股数
            #print(prediction)
            if prediction == 1:
                buy_price = close_price_k[temp_index]#记录买价
                if close_price_k[temp_index]> close_price_k[len(close_price_k)-1]:
                    isRight.append(-1)
                if close_price_k[temp_index]<= close_price_k[len(close_price_k)-1]:
                    isRight.append(1)
                temp_index = temp_index +1
                fill_price.append(buy_price)#记录成交价
                tv.append(buy_price*per_trade_volume)#本次成交额
                comission.append(buy_price*commision_ratio*per_trade_volume)#记录交易费用
                position = position + per_trade_volume#记录持仓量
                position_s.append(position)
                busy_type.append("buy")
                temp_profit=-buy_price*commision_ratio*per_trade_volume - buy_price*per_trade_volume
                profit.append(temp_profit)             
            else:
                sell_price =  close_price_k[temp_index]#记录卖价
                if close_price_k[temp_index]>= close_price_k[len(close_price_k)-1]:
                    isRight.append(1)
                if close_price_k[temp_index]< close_price_k[len(close_price_k)-1]:
                    isRight.append(-1)
                temp_index = temp_index +1
                fill_price.append(sell_price)#记录成交价
                tv.append(sell_price*per_trade_volume)#记录成交额
                comission.append(sell_price*per_trade_volume*(commision_ratio+tax_ratio))#记录交易费用
                position = position - per_trade_volume#记录持仓量
                position_s.append(position)
                busy_type.append("sell")
                temp_profit = -sell_price*per_trade_volume*(commision_ratio+tax_ratio) + sell_price*per_trade_volume
                profit.append(temp_profit)
        #日末平仓
        profit_end = 0
        busy_type.append("close")
        fill_price.append(close_price_k[len(close_price_k)-1])
        predictions.append(0)
        
        for i in range(0,len(fill_price)):
            if busy_type[i]=="buy":
                profit_end = profit_end - tv[i]-comission[i]
            if busy_type[i]=="sell":
                profit_end = profit_end + tv[i] - comission[i]
        #日末还有持仓 以日未收盘价卖出平仓
        if position>0:
            close_end = close_price_k[len(close_price_k)-1]
            comission_end = close_end*position*(commision_ratio+tax_ratio)
            comission.append(comission_end)
            tv.append(close_end*position)
            profit_end = close_end*position - comission_end
            profit.append(profit_end)
        if position<0:
            close_end = close_price_k[len(close_price_k)-1]
            comission_end = close_end*(0-position)*commision_ratio
            comission.append(comission_end)
            tv.append(close_end*(0-position))
            profit_end= - close_end*(0-position) - comission_end
            profit.append(profit_end)
        position_s.append(0)
        countIsRight = 0.0
        countIsError = 0.0
        for i in range(len(isRight)-len(open_price_k),len(isRight)-1):
            if isRight[i]==1:
                countIsRight = countIsRight +1
            if isRight[i]==-1:
                countIsError = countIsError + 1
        isRight.append(countIsRight/(countIsRight+countIsError))
        pn_profit=[]#收益，k线内累计收益

        
        for i in range(0,len(profit)):
            
            temp_sum = 0
            for j in range(0,i+1):
                temp_sum = temp_sum + profit[j]
            pn_profit.append(temp_sum)
                
        #组织交易记录表
        daily_trade_record = {
            "symbol":k_bar["symbol"],
            "date":k_bar["date"],
            "time":k_bar["eob"].apply(lambda x:x[11:]),
            "busy_type":busy_type,
            "fill_price":fill_price,
            "comission":comission,
            "tv":tv,
            "position_s":position_s,
            "profit":profit,
            "pn_profit":pn_profit,
            "isRight":isRight,
            "predictions":predictions
        }
        columns = ["symbol","date","time","busy_type","fill_price","comission","tv","position_s","profit","pn_profit","isRight","predictions"]
        daily_trade_record = DataFrame(daily_trade_record,columns=columns)
        days_trade_record = pd.concat([days_trade_record,daily_trade_record],axis=0) #将当日交易记录加入多日交易记录
        
        
out_file_path="E:/test_data/result/"+symbol+"/"+symbol+"_trade_record.csv"
days_trade_record.to_csv(out_file_path,index=None) #输出交易记录

pic_path="E:/test_data/result"

    
    

print("~√~谢谢")



if(not os.path.exists(pic_path)):
        os.mkdir(pic_path)

for date in days_trade_record[days_trade_record["time"]=="15:00:00"]["date"].drop_duplicates():
    daily_record = days_trade_record[days_trade_record["date"]==str(date)]
    color_collection = {"0":"#054E9F","1":"red","-1":"lime"}
    linestyle_collection = {"0":"-","1":"--","-1":"--"}
    linewidth_collection = {"0":2.0,"1":3.0,"-1":3.0}
    y = daily_record["fill_price"].values
    x = daily_record.index.values
    plt.plot(x,y)
    plt.savefig("E:/test_data/result/"+symbol+"/fillPrice/"+date+".png")
    plt.cla()
    
    x = daily_record.index.values
    yIsRight = daily_record["isRight"].values
    plt.figure(1)
    p1=plt.scatter(x,yIsRight,marker='*',color='r',label='1',s=30)
    plt.savefig("E:/test_data/result/"+symbol+"/isRight/"+date+".png")
    plt.cla()
    print("xixi")
    
print("thanks")