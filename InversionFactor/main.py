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
        print(len(code_list))
        # 当日结果因子值
        result = []
        # 当日结果code值
        result_code = []
        # 针对每一个code进行计算因子值
        for j in range(0, len(code_list)):
            # 获取每个code对应的前n天数据
            now_day_code_data = n_day_data[n_day_data['code'] == code_list[j]]
            # print(now_day_code_data['trade_dt'])
            # print(len(now_day_code_data['trade_dt']))
            # 如果数据满足n天，进行计算
            if len(now_day_code_data) == n:
                # 记录满足的code
                result_code.append(code_list[j])
                # 平均单笔成交金额
                d_list = now_day_code_data['amount'] / now_day_code_data['count']

                # 获取相应code当前所需的 d_list, pct_change_list
                d_list = d_list.values
                pct_change_list = now_day_code_data['pct_change'].values

                # 对d_list进行排序(从大到小，相应调整pct_change_list)
                for index1 in range(0, n-1):
                    for index2 in range(index1+1, n):
                        if d_list[index1] < d_list[index2]:
                            # 交换d_list
                            temp_swap_d = d_list[index1]
                            d_list[index1] = d_list[index2]
                            d_list[index2] = temp_swap_d
                            # 交换pct_change_list
                            temp_swap_pct_change = pct_change_list[index1]
                            pct_change_list[index1] = pct_change_list[index2]
                            pct_change_list[index2] = temp_swap_pct_change

                # 计算M_high
                m_high = 1
                for k in range(0, int(n/2)):
                    m_high = m_high * (1 + pct_change_list[k])
                m_high = m_high - 1
                print(m_high)
                # 计算M_low
                m_low = 1
                for k in range(int(n/2), n):
                    print(k)
                    m_low = m_low * (1 + pct_change_list[k])
                m_low = m_low - 1
                print(m_low)
                result.append(m_high - m_low)
        day_calculate_data = pd.DataFrame({'code': result_code, 'm': result})
        day_calculate_data.to_csv("F:/data/result/" + str(date_list[i]) + ".csv", index=False, sep=',')


if __name__ == '__main__':
    file_path = "F:/data/成交金额成交笔数/count_amount_data.csv"
    inversion_factor_calculate(file_path, 20)
