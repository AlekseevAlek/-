import pandas as pd

#Функция выводит среднюю цену закрытия акций за заданный период.
def calculate_and_display_average_price(data):

    data = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {data}")


#Функция анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
def notify_if_strong_fluctuations(data, threshold=15):

    percent = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if percent >= threshold:
        print(f'цена акций колебалась на {percent}%')


