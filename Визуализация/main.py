import pandas as pd
import matplotlib.pyplot as plt  # объект pyplot - пайтон график
import seaborn as sns

workouts = pd.read_csv('workouts.csv', parse_dates=['start_at'])
users = pd.read_excel('users.xlsx')

workouts_users = pd.merge(
    workouts,
    users,
    how='left',
    left_on='client_id',
    right_on='user_id'
)

payments = pd.read_excel('payments.xlsx')
marketing = pd.read_excel('marketing.xlsx')


payments['payment_datetime'] = pd.to_datetime(payments['payment_date'])  # переводим даты в нужный формат
payments_with_geo = pd.merge(payments,
                             users[['user_id', 'geo_group']],
                             on='user_id')  # объединяем платежи и данные о географии студентов

fst_payment = payments_with_geo.groupby(['user_id', 'geo_group'])['payment_date'].min()  # вычисляем даты первых оплат для каждого клиента
fst_payment = fst_payment.reset_index()  # сбрасываем индекс
fst_payment_month = fst_payment.groupby(
    [fst_payment['payment_date'].dt.month,
     fst_payment['geo_group']])['user_id'].count().reset_index()  # считаем количество первых оплат в каждом месяце и гео-группе

fst_payment_month.columns = ['month', 'geo_group', 'sales']  # меняем заголовки

marketing_sales = pd.merge(
    fst_payment_month,
    marketing,
    on=['geo_group', 'month'])

marketing_sales_total = marketing_sales.groupby('month')[['sales', 'budget']].sum().reset_index()  # сумма двух колонок 'sales', 'budget'
geo_groups = set(marketing_sales['geo_group'])


# colors = {
#     'Москва': 'c',
#     'Регионы РФ': 'tab:olive',
    # 'СНГ': 'r',
    # 'Без страны': 'k'
    # }

# СТРОИМ ТОЧЕЧНЫЙ ГРАФИК #

# можно так отобразить х и у (The best way)
# plt.scatter(
#     marketing_sales_total['budget'],  # значения оси х
#     marketing_sales_total['sales'],  # значения оси e
#     alpha=0.7
# )

# а можно так (not likely)
plt.figure(figsize=(10, 5))  # размер графика в дюймах ширина, длина ПИСАТЬ ВСЕГДА ПОСЛЕ НАСТРОЕК, ДО ПОСТРОЕНИЯ ГРАФИКА
# plt.xlim(-10_000, 1_000_000)
# plt.ylim(0, 250)


# plt.scatter(
#     marketing_sales_total.budget,  # значения оси х
#     marketing_sales_total.sales,  # значения оси e
#     # c=marketing_sales['geo_group'].map(colors),  # доп аргумент (ИМЕННО с) с равный столбцу из датафрейма
#     alpha=0.5,  # прозрачность точек, в данном случае прозрачность = 30%, по умолчанию прозрачности нет, т.е альфа равна 1
#     marker='*',
#     )

# plt.title('Зависимость количество привлеченных клиентов от затрат на маркетинг (помесячно)')
# plt.xlabel('Затраты на маркетинг, р')
# plt.ylabel('Первых покупок')
# plt.grid()   # выводит сетку

# plt.show()  # вывод графика


# СТРОИМ ЛИНЕЙНЫЙ ГРАФИК #

workout_by_week = workouts.resample('W', on='start_at')['workout_id'].count()


def get_season(date):
    month = date.month
    if month in (3, 4, 5):
        return 'Весна'
    elif month in (6, 7, 8):
        return 'Лето'
    elif month in (9, 10, 11):
        return 'Осень'
    else:
        return 'Зима'


workout_by_week_seasons = workout_by_week.reset_index().iloc[:-1]
workout_by_week_seasons['season'] = workout_by_week_seasons['start_at'].apply(get_season)
# print(workouts)

colors_seasons = {
    'Зима': 'b',
    'Осень': 'r',
    'Лето': 'g',
    'Весна': 'y'}


plt.title('Распределение количества тренировок по неделям')
plt.xlabel('Дата')
plt.ylabel('Кол-во тренировок')
plt.grid()

# plt.plot(workout_by_week_seasons['start_at'],
#          workout_by_week_seasons['workout_id']
#          )  # по оси Х  будет индекс - дата

plt.scatter(
    workout_by_week_seasons.start_at,  # ось Х
    workout_by_week_seasons.workout_id,  # ось Y
    c=workout_by_week_seasons['season'].map(colors_seasons)
)

# plt.show()  # вывод графика

# СТРОИМ ГИСТОГРАММУ #
# client_week_workouts = workouts[
#     (workouts.status == 'success') &
    # (workouts.workout_shedule_type != 'trial')
# ]
# client_id = workouts['client_id']
# weeks = workouts['start_at'].dt.week
#
# client_week_workouts = client_week_workouts.groupby(
#     [client_id, weeks]
# )['workout_id'].count().reset_index()
#
# avg_workouts_per_week = client_week_workouts.groupby('client_id')['workout_id'].mean()
# print(avg_workouts_per_week.head())

plt.figure(figsize=(10, 5))
plt.title('Распределение среднего недельного количества тренировок')
plt.xlabel('Кол-во тренировок в неделю')
plt.ylabel('Кол-во клиентов')
plt.grid()

# plt.hist(avg_workouts_per_week, bins=50)

# plt.show()

# СТРОИМ ЯЩИК С УСАМИ #
# revenue_per_month = payments.resample('M', on="payment_date")['amount'].sum() / 1_000_000
# revenue_per_week = payments.resample('W', on="payment_date")['amount'].sum() / 1_000_000
# revenue_per_day = payments.resample('D', on="payment_date")['amount'].sum() / 1_000

revenue_by_day_month = payments.groupby(
    [payments['payment_date'].dt.day,
     payments['payment_date'].dt.month]
)
# revenue_by_day_month.index.names = ['day', 'month']  # группировка создает мультиячейку
# revenue_by_day_month = revenue_by_day_month.reset_index()

plt.figure(figsize=(10, 5))
plt.title('Распределение кол-ва выручки по неделям')
plt.grid()

sns.boxplot(
    x='month',
    y='amount',
    data=revenue_by_day_month,
    color='y'
)

# sns.boxplot(x=revenue_per_day,
#             color='c')

plt.xlabel('Выручка в день')  # в seaborn ось подписывается после
plt.ylabel('Месяц')

plt.show()

