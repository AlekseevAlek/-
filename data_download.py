import yfinance as yf


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

def rsi(data, periods = 12 ):
    close_delta = data['Close'].diff()

    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.rolling(window=periods).mean()
    ma_down = down.rolling(window=periods).mean()

    rs = ma_up / ma_down
    rsi = 100 - 100 / (1+rs)
    data['RSI']=rsi

    return data

