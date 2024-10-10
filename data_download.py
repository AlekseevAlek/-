import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go


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


def create_interactive_plot(data):
    '''Функция создаёт интерактивный график'''
    # Вычисляем среднее значение колонки 'Close'
    avg_price = data['Close'].mean()

    # Создаем график с использованием Plotly
    fig = go.Figure()

    # Добавляем линейный график для цены закрытия
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия'))

    # Добавляем линейный график для скользящего среднего
    fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'], mode='lines', name='Скользящее среднее'))

    # Добавляем текст с информацией о средней цене
    fig.add_annotation(text=f'Средняя цена: {avg_price:.2f}', x=0.5, y=0.95, showarrow=False,
                       xanchor='center', yanchor='top')

    # Настройка осей и заголовок
    fig.update_layout(title='Цена акций и Скользящее Среднее',
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      hovermode='x unified',
                      width=1200,
                      height=800
                      )

    # Ограничение диапазона оси X
    max_date = max(data.index)
    min_date = min(data.index)
    fig.update_xaxes(range=[min_date, max_date])

    # Отображаем интерактивный график
    fig.show()
