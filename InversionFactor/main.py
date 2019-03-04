import pandas as pd


# 功能 ： 进行反转因子值的计算
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
    for i in range(n,len(date_list)):
        print("today:"+str(date_list[i]))
        # 获取当前天的 n天前的所有数据




if __name__ == '__main__':
    file_path = "F:/data/成交金额成交笔数/count_amount_data.csv"
    inversion_factor_calculate(file_path, 20)
