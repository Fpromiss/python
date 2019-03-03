import pandas as pd


# 功能 ： 进行反转因子值的计算
# @param ：data_path ：数据文件路径
# @param ：n ：计算交易日天数
def inversion_factor_calculate(data_path, n):
    # 获取所有数据
    all_data = pd.read_csv(data_path)
    # 清洗空数据
    clear_data = all_data.dropna(axis=0, how='any', inplace=False)
    # 获取所有code
    code_list = clear_data['code'].groupby(clear_data['code']).first()
    for code in code_list:
        print(code)
        # 获取当前code的所有相关数据
        code_data = clear_data[clear_data['code'] == code]
        print(code_data)
        break


if __name__ == '__main__':
    file_path = "F:/data/成交金额成交笔数/count_amount_data.csv"
    inversion_factor_calculate(file_path, 20)
