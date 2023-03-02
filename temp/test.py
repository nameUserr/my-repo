import pandas as pd
from pandas import Series
l = [1,2,3,4,5]
print(l == 1)
s = Series(l)
print(s == 1)
print(pd.cut(s, bins=[0, 2, 4, 6]))