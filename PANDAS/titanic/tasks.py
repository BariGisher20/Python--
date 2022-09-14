import pandas as pd
import numpy as np

dict_1 = {'a': 100, 'b': 200, 'c': 300, 'd': 400, 'e': 800}
np_array = np.array([10, 20, 30, 40, 50])

ds_1 = pd.Series([2, 4, 6, 8, 10])
ds_2 = pd.Series([1, 3, 5, 7, 9])
ds_3 = pd.Series(dict_1)
df_1 = pd.DataFrame({
    'col1': [1, 2, 3, 4, 7, 11],
    'col2': [4, 5, 6, 9, 5, 0],
    'col3': [7, 5, 8, 12, 1, 11]})
s_1 = pd.Series(df_1['col1'])

ser_1 = pd.Series(['100', '200', 'python', '300.12', '400'])
ser_to_array = np.array(ser_1)

print(ser_to_array)
