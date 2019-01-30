from __future__ import print_function, absolute_import, unicode_literals
from datetime import datetime
import math
from sklearn import svm
import pandas as pd
import os
from pandas import DataFrame
import matplotlib.pyplot as plt




if __name__ == '__main__':
    print("train")
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
