import pandas as pd
from pandas import Series
import numpy as np

# 设定pandas的float类型显示精度
pd.set_option('display.float_format',lambda x : '%.20f' % x)

def print_prompt(prompt:str):
    line = '-' * 20
    print(line + prompt + line)

def filter_extreme_3sigma(x: Series, n=3):
    mean = x.mean()
    std = x.std()
    max_range = mean + n * std
    min_range = mean - n * std
    return np.clip(x, min_range, max_range), len(x[x < min_range]), len(x[x > max_range])

def normalize_to_one(x: Series):
    return (x - x.min()) / (x.max() - x.min())

def proc(x: Series, bins):
    # 对数缩放
    x_scaled = np.log(x)
    # 修剪极值
    x_filtered, min_clip_count, max_clip_count = filter_extreme_3sigma(x_scaled)
    # 归一化
    x_normalized = normalize_to_one(x_filtered)
    # 分组
    x_bin_cut = pd.cut(x_normalized, bins, include_lowest=True)
    # 获取组别
    x_bin_indices = [int(i.right * 4) for i in x_bin_cut]
    return x_scaled, x_filtered, x_normalized, x_bin_indices

if __name__ == '__main__':
    # sql = "WITH mdm_zzs_mf as ( SELECT compid, orgobjnamegl, compname_abbr,mzm.lev, zzlb,unit_name,extend_field_1 FROM dim_fin_gw_010100_zzs_final_mf mzm where unit_name= '供电分公司' and zzdxsfzs= '是' and lev = '4' and sfhzqz= '是' and tyear= '2022' ),ywzb as (SELECT a.compid ,a.tmonth,a.compname, a.compname_abbr, a.heji, c.bnljs FROM ( select case when compname_abbr='国家电网公司' then '国网' when compname_abbr='黑龙江' then '龙江' else compname_abbr end as compname_abbr,compname, tmonth, compid , sum(heji) heji, ywfl1048dl FROM ADS_FIN_GW_010101_12_1_4_DWYWZB_MF WHERE cjno='12.1.4' and changjing='本年累计' and ywfl1048dl = '营销' and tmonth = '202212' group by case when compname_abbr='国家电网公司' then '国网' when compname_abbr='黑龙江' then '龙江' else compname_abbr end , tmonth, compid , ywfl1048dl,compname )a left join ( SELECT compid,bnljs FROM self_ads_fin_gw_010100_bbsj c where zbmc = '售电量_还原' and concat(substr(c.ttime,1,4),substr(c.ttime,6,2)) = '202212' )c on a.compid = c.compid ) SELECT a.compid,a.orgobjnamegl, a.compname_abbr,a.extend_field_1,a.zzlb,a.unit_name, b.tmonth,b.heji/100000000,b.bnljs ,b.heji/b.bnljs/100 as ddyxcb FROM ywzb b join mdm_zzs_mf a on a.compid=b.compid;"
    target_names = ['售电量(千瓦时)', '度电营销成本(分千瓦时)']
    filter_col = '单位简称'
    bins = [0, 0.25, 0.5, 0.75, 1]
    bin_indices = [1, 2, 3, 4]

    # print_prompt('执行sql')
    # print(sql)
    data = pd.read_excel('度电营销成本(售电量)-带SQL.xlsx')
    # 转换数据格式
    for t in target_names:
        data[t] = data[t].astype(float)
    # 剔除空值和负值
    data = data[(data[target_names[0]] > 0) & (data[filter_col].notnull()) & (data[target_names[1]] > 0)]
    print_prompt('sql执行结果')
    print(data)
    print_prompt('结果信息-info')
    print(data.info())
    print_prompt('结果统计信息')
    print(data.describe())
    # 提取目标列
    y = data[target_names[0]]
    yy = data[target_names[1]]

    y_scaled, y_filtered, y_normalized, y_bin_indices = proc(y, bins)
    data[target_names[0] + '_对数缩放'] = y_scaled
    data[target_names[0] + '_修剪极值'] = y_filtered
    data[target_names[0] + '_归一化'] = y_normalized
    data[target_names[0] + '_分组'] = y_bin_indices
    # 分组计数
    print_prompt(target_names[0] + '分组计数')
    print(Series(y_bin_indices, dtype='int').value_counts().sort_index())
    yy_ranges = []
    for i in bin_indices:
        ss = yy.iloc[(Series(y_bin_indices, dtype='int') == i).to_list()]
        yy_ranges.append([ss.min(), ss.max()])
    yy_bin_indices = []
    yy_normalized = []
    for i in range(len(yy)):
        norm = (yy.iloc[i] - yy_ranges[y_bin_indices[i] - 1][0]) / (yy_ranges[y_bin_indices[i] - 1][1] - yy_ranges[y_bin_indices[i] - 1][0])
        yy_normalized.append(norm)
        for b in bins:
            if norm <= b:
                yy_bin_indices.append(int(b * 4))
                break
    data[target_names[1] + '_归一化'] = yy_normalized
    data[target_names[1] + '_分组'] = yy_bin_indices
    print_prompt('分组结果')
    print(data.to_string())