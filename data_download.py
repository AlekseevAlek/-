import yfinance as yf
import pandas as pd
from datetime import datetime


def fetch_stock_data(ticker, start_date, end_date):
    '''Функция получает исторические данные об акциях для указанного тикера и временного периода. Возвращает DataFrame
     с данными.'''
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data


def add_moving_average(data, window_size=5):
    '''Функция добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия.'''
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    '''Функция выводит среднюю цену закрытия акций за заданный период'''

    data = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {data}")


def notify_if_strong_fluctuations(data, threshold=15):
    '''Функция анализирует данные и уведомляет пользователя,
    если цена акций колебалась более чем на заданный процент за период'''

    percent = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if percent >= threshold:
        print(f'цена акций колебалась на {percent}%')


def export_data_to_csv(data, filename):
    '''Функция сохраняет загруженные данные об акциях в CSV файл.'''

    data = data['Close']
    data.to_csv(filename)


def add_technical_indicators(data):
    '''Функция добавляет дополнительный технический индикатор RSI'''

    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_std(data, window_size=20):
    '''Функция добавляет статистический индикатор - стандартное отклонение цены закрытия.'''

    data['STD'] = data['Close'].rolling(window=window_size).std()
    return data
