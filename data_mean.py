import pandas as pd


def calculate_and_display_average_price(data):
    '''Функция выводит среднюю цену закрытия акций за заданный период'''

    data = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {data}")



def notify_if_strong_fluctuations(data, threshold=15):
    '''Функция анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период'''

    percent = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if percent >= threshold:
        print(f'цена акций колебалась на {percent}%')


def export_data_to_csv(data, filename):
    '''Функция сохраняет загруженные данные об акциях в CSV файл.'''

    data = data['Close']
    data.to_csv(filename)

