import pandas as pd
from pandas import Series

s = Series([1,2,3,4,5])
print(pd.cut(s, bins=[2, 4, 6]))