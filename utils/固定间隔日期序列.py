import pandas as pd
import numpy as np
try:
    print(pd.date_range('2022-01', '2023-01', freq = 'M').strftime('%Y%m').to_list())
    raise Exception('sdf')
except Exception as e:
    print(e)