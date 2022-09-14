import pandas as pd
import matplotlib.pyplot as plt


titanic_df = pd.read_csv('titanic.csv')
pvt = titanic_df.pivot_table(
    index=['Sex'],
    columns=['PClass'],
    values='Name',
    aggfunc='count'
)

# print(pvt.loc[['female'], ['1st', '2nd', '3rd']])

apple_df = pd.read_csv('apple.csv', index_col='Date', parse_dates=True)
apple_df = apple_df.sort_index()
apple_df.loc['2012-Feb', 'Close'].mean()  # средняя цена акций за 2012 февраля при закрытии
apple_df.loc['2012-Feb': '2015-Feb', 'Close'].mean()  # средняя цена акций с 2012 по 2015 февраля при закрытии

apple_df.resample('W')['Close'].mean()  # по неделям

apple_df.loc['2012-Feb': '2015-Feb', 'Close'].plot()
plt.show()
# print(apple_df.resample('W')['Close'].mean())


