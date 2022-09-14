import pandas as pd

a = pd.Series([2, 4, 6, 8])
b = pd.Series([1, 3, 5, 7])

res = sum((a-b)*(a-b))**0.5
print(res)
