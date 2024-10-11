import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from main import graph_folder


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    '''Функция создаёт график, отображающий цены закрытия, скользящие средние, RSI, STD. Предоставляет возможность
     сохранения  графика в файл. '''

    plt.figure(figsize=(10, 6))
    # Проверяем существование файла стиля
    custom_style_file = f"{style}.mplstyle"
    if os.path.exists(custom_style_file):
        plt.style.use(custom_style_file)
    else:
        plt.style.use('default')

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            plt.plot(dates, data['RSI'].values, label='RSI')
            plt.plot(dates, data['STD'].values, label='STD')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.plot(data['Date'], data['RSI'], label='RSI')
        plt.plot(data['Date'], data['STD'], label='STD')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    #if filename is None:
        #filename = f"{ticker}_{period}_stock_price_chart.{style.lower()}.png"



    #plt.savefig(filename, format='png')
    #print(f"График сохранен как {filename}")

    # Генерируем имя файла на основе тикера и периода
    base_filename = f"{ticker}_{period}_stock_price_chart"

    # Если имя файла не указано явно, используем базовое имя
    if filename is None:
        filename = f"{base_filename}.{style.lower()}.png"
    else:
        filename = f"{filename}.{style.lower()}.png"

    # Создаем путь для графика в папке graph_folder
    graph_path = os.path.join(graph_folder, filename)

    # Сохраняем график в отдельную папку
    plt.savefig(graph_path, format='png')
    print(f"График сохранен как {graph_path}")

    # Очищаем фигуру после сохранения
    plt.clf()