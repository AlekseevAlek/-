import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

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


def add_technical_indicators(data):
    # Рассчитываем RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Создаем DataFrame с индикаторами
    indicators = pd.DataFrame({
        'RSI': rsi})

    # Объединяем исходные данные с индикаторами
    combined_data = pd.concat([data, indicators], axis=1)
    return combined_data

def download_and_process_data(ticker, period):
    data = fetch_stock_data(ticker, period)
    processed_data = add_technical_indicators(data)
    return data['Close'], processed_data