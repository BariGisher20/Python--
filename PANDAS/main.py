import pandas as pd
import uni


workouts = pd.read_csv('workouts.csv')
payments = pd.read_excel('payments.xlsx')
users = pd.read_excel('users.xlsx')
workouts.reset_index()
# print(users.loc[[4268, 4272]])  # достаем данные из строк 4268 и 4272
# print(users.loc[[4268, 4272], ['region', 'first_contact_datetime']])  # достаем только столбцы region и first_contact_datetime для строк 4268 и 4272
# print(users.loc[users['geo_group'] == 'Москва'])  # фильтрация данных по городу Москва
# print(users.loc[users['age'] <= 30.0].head)  # выведет все данные о пользователях младше 30 (включительно)
pd.to_datetime(payments['payment_date'])  # изменили данные в колонке, но только на эту итерацию, в DataFrame они не изменились
payments['payment_date'] = pd.to_datetime(payments['payment_date'])  # изменили данные в DataFrame
workouts['start_at'] = pd.to_datetime(workouts['start_at'])
users.groupby('geo_group')['age'].max()  # находим максимальный возраст тренирующихся по гео-группе
workouts.groupby('trainer_department')['client_id'].nunique()  # узнаем кол-во клиентов у которых занятия проводили тренеры из разных департаментов
workouts.reset_index(inplace=True)  # переносим индекс в колонку
workouts.groupby('trainer_department')['workout_id'].nunique()  # какое кол-во занятий провели тренеры разных департаментов
workouts.groupby(['trainer_department', 'workout_type'])['workout_id'].nunique()  # какое кол-во занятий провели тренеры разных департаментов по разным типам тренировок
workouts['client_id'].groupby(workouts['start_at'].dt.month).nunique()  # сколько клиентов пришли на тренировки помесячно
workouts['cost'].agg(['count', 'mean', 'median'])  # выводим сразу несколько показателей (только те, что нам нужны)
workouts.agg(
    {
        'cost': ['count', 'mean', 'median'],
        'workout_id': ['count', 'nunique']
    }
)  # считаем для разных столбцов разные статистики (показатели/ агрегаты)

first_payments = payments.groupby('user_id')['payment_date'].min()
first_workout = workouts.groupby('client_id')['start_at'].min()
# pd.merge(payments, users)  # объединение таблиц
workouts_users = pd.merge(workouts, users, how='left', left_on='client_id', right_on='user_id')

first_payments = first_payments.reset_index()
first_workout = first_workout.reset_index()
users_info = pd.merge(first_payments, first_workout, how='inner', left_on='user_id', right_on='client_id')

# добавление колонок
payments['version'] = 1
payments['fix_rate'] = 73
payments['amount_usd'] = payments['amount'] / payments['fix_rate']

users_info['date_diff'] = users_info['payment_date'] - users_info['start_at']
users_info.sort_values(by='date_diff')  # сортировка по колонке date_diff по умолчанию (по возрастанию)
users_info.sort_values(by='date_diff', ascending=False)  # сортировка по колонке date_diff по убыванию


mean_value = users_info['date_diff'].mean()
def checher(datediff_in_days):
    if datediff_in_days < mean_value:
        return 'Быстрый'
    else:
        return 'Медленный'


users_info['client_type'] = users_info['date_diff'].apply(checher)

users_info.to_excel('user_info.xlsx')

writer = pd.ExcelWriter('all_data.xlsx')
users_info.to_excel(writer, sheet_name='payments')
payments.to_excel(writer, sheet_name='payments')
users.to_excel(writer, sheet_name='users')
workouts.to_excel(writer, sheet_name='workouts')

writer.save()


print(users_info)


