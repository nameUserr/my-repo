import pandas as pd
import numpy as np

def normalize_zero_one(x):
    # Check whether input data is 1 dimensional
    x_dim = getattr(x, 'ndim', None)
    if x_dim is None:
        x = np.asarray(x)
    if x_dim != 1:
        raise ValueError('Input array must be 1 dimensional')
    return (x - x.min()) / (x.max() - x.min())

def get_bin_count(x, bins):
    return pd.cut(x, bins, include_lowest=True).value_counts().sort_index().to_list()

def main():
    data = pd.read_excel("../示例数据.xlsx")
    sheng = data['财务管控所属二级单位']
    val = data['指标值'].replace(np.nan, 0)
    for i in range(len(val)):
        if val[i] < 0:
            val[i] = 0
    bins = [0, 0.25, 0.5, 0.75, 1]
    val_norm = normalize_zero_one(val)
    gw_bin_count = get_bin_count(val_norm, bins)
    bin_count = pd.DataFrame({
        'sheng': [],
        '[0, 0.25]': [],
        '(0.25, 0.5]': [],
        '(0.5, 0.75]': [],
        '(0.75, 1]': []
    })
    bin_count.loc[len(bin_count)] = ['国网',] + gw_bin_count
    provinces = sheng.drop_duplicates()
    for p in provinces:
        p_val = []
        for i in range(len(data)):
            if sheng[i] == p:
                p_val.append(val_norm[i])
        p_bin_count = get_bin_count(pd.Series(p_val), bins)
        bin_count.loc[len(bin_count)] = [p,] + p_bin_count
    print(bin_count)

if __name__ == '__main__':
    main()
    # np.random.seed(0)
    # data = pd.DataFrame(np.random.RandomState(0).randint(0, 100, size=(50, 3)))
    # print(normalize_zero_one(pd.Series(data[0].tolist())))