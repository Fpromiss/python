import pandas as pd


# 功能 ： 进行反转因子值的计算
# 文件 表头 ：  code  trade_dt  pct_change      amount    count
# @param ：data_path ：数据文件路径
# @param ：n ：计算交易日天数
def inversion_factor_calculate(data_path, n):
    # 获取所有数据
    all_data = pd.read_csv(data_path)
    # 清洗空数据
    clear_data = all_data.dropna(axis=0, how='any', inplace=False)
    # 获取所有日期
    date_list = clear_data['trade_dt'].groupby(clear_data['trade_dt']).first()
    date_list = date_list.values
    # 针对每一天（针对因子计算应该从第n+1天开始）
    for i in range(n, len(date_list)):
        print("today:"+str(date_list[i]))
        # 获取当前天的 n天前的所有数据
        print(date_list[i-n])
        print(date_list[i])
        n_day_data = clear_data[(clear_data['trade_dt'] >= date_list[i - n]) & (clear_data['trade_dt'] < date_list[i])]
        # 获取所有code
        code_list = n_day_data['code'].groupby(n_day_data['code']).first()
        code_list = code_list.values
        # 当日结果
        result = []
        # 针对每一个code进行计算因子值
        for j in range(0, len(code_list)):
            # 获取每个code对应的前n天数据
            now_day_code_data = n_day_data[n_day_data['code'] == code_list[j]]
            d = []  # 平均单笔成交金额
            print(now_day_code_data['trade_dt'])
            print(len(now_day_code_data['trade_dt']))
            #for j in range(0, len(now_day_code_data)):

        break


if __name__ == '__main__':
    file_path = "F:/data/成交金额成交笔数/count_amount_data.csv"
    inversion_factor_calculate(file_path, 20)
