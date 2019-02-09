import numpy as np
import math


# 计算 x1
# @param ：yes_open_price_day ：昨日开盘价
# @param ：close_price_k ：今日5分钟k线最新收盘价
# @return ：x1  昨日开盘价 / 最新收盘价 - 1
def calculate_x1(yes_open_price_day, close_price_k):
    return yes_open_price_day / close_price_k - 1


# 计算 x2
# @param ：yes_close_price_day ：昨日收盘价
# @param ：close_price_k ：今日5分钟k线最新收盘价
# @return ：x2  昨日收盘价 / 最新收盘价 - 1
def calculate_x2(yes_close_price_day, close_price_k):
    return yes_close_price_day / close_price_k - 1


# 计算 x3
# @param ：yes_high_price_day ：昨最高价
# @param ：close_price_k ：今日5分钟k线最新收盘价
# @return ：x3  昨日最高价 / 最新收盘价 - 1
def calculate_x3(yes_high_price_day, close_price_k):
    return yes_high_price_day / close_price_k - 1


# 计算 x4
# @param ：yes_low_price_day ：昨日最低价
# @param ：close_price_k ：今日5分钟k线最新收盘价
# @return ：x4  昨日最低价 / 最新收盘价 - 1
def calculate_x4(yes_low_price_day, close_price_k):
    return yes_low_price_day / close_price_k - 1


# 计算 最新成交量 ： 最新成交量 = 今日最新累计成交量 * 日总k线数 / 开盘至今当前k线数
# @param ：new_volume_k ：今日最新累计成交量
# @param ：ri_zong_k_num ：日总k线数
# @param ：new_k_num ：开盘至今当前k线数
# @return ：最新成交量
def calculate_new_volume(new_volume_k, ri_zong_k_num, new_k_num):
    return new_volume_k * ri_zong_k_num / new_k_num


# 计算 x5
# @param ：yes_volume ：昨日成交量
# @param ：new_volume_k ：今日5分钟k线最新成交量 ： 最新成交量 = 今日最新累计成交量 * 日总k线数 / 开盘至今当前k线数
# @return ：x5  最新成交量 / 昨日成交量 - 1
def calculate_x5(yes_volume, new_volume_k):
    return new_volume_k / yes_volume - 1


# 计算昨日波动率
# @param ：yes_close_price_k ：昨日5分钟k线数据
def calculate_yes_bo_dong_lv(yes_close_price_k):
    return np.std(yes_close_price_k)


# 计算最新波动率
# @param ：new_close_price_k ：今日5分钟k线数据（到最新/当前为止）
# @param ：ri_zong_k_num ：日总k线数
# @param ：new_k_num ：开盘至今k线数
def calculate_new_bo_dong_lv(new_close_price_k, ri_zong_k_num, new_k_num):
    result = np.std(new_close_price_k)
    xi_shu = math.sqrt(ri_zong_k_num/new_k_num)
    return result*xi_shu


# 计算 x6
# @param ：yes_bo_dong_lv ： 昨日波动率
# @param ：new_bo_dong_lv ： 最新波动率
# @return ：x6  最新波动率 / 昨日波动率 - 1
def calculate_x6(yes_bo_dong_lv, new_bo_dong_lv):
    return new_bo_dong_lv / yes_bo_dong_lv - 1


# 计算 x7
# @param ：today_open_price_day ：今日开盘价
# @param ：new_close_price_k ： 最新收盘价
# @return ： x7 ： 今日开盘价 / 最新收盘价 - 1
def calculate_x7(today_open_price_day, new_close_price_k):
    return today_open_price_day / new_close_price_k - 1


# 计算 x8
# @param ： new_high_price_k ：今日5分钟k线最高价
# @param ：new_close_price_k ：今日5分钟k线最新收盘价
# @return ： x8 ：最新最高价 / 最新收盘价 - 1
def calculate_x8(new_high_price_k, new_close_price_k):
    return new_high_price_k / new_close_price_k - 1


# 计算 x9
# @param ： new_low_price_k ：今日5分钟k线最新最低价
# @param ：new_close_price_k ：今日5分钟k线最新收盘价
# @return ： x9 ： 最新最低价 / 最新收盘价 - 1
def calculate_x9(new_low_price_k, new_close_price_k):
    return new_low_price_k / new_close_price_k - 1


# 计算 y
# @param ：today_close_price_day ：今日收盘价
# @param ：new_close_price_k ：最新收盘价
# @return ：如果今日收盘价大于最新收盘价，说明涨了，返回1; 反之说明跌了，返回-1
def calculate_y(today_close_price_day, new_close_price_k):
    if today_close_price_day > new_close_price_k:
        return 1
    else:
        return -1

