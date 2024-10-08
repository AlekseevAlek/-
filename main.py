import data_download as dd
import data_plotting as dplt
import pandas as pd
from datetime import datetime, timedelta


def main():
    global start_date, end_date
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet "
        "Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, "
        "с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")

    '''Пользователь может ввести даты в формате YYYY-MM-DD или использовать предустановленные периоды'''
    period_input = input(
        "Введите период для данных (например, '2020-01-01 2020-12-31' для данных за 2020 год, или '1mo' для одного "
        "месяца): ")

    '''Обработка ввода пользователя'''
    if '-' in period_input:
        start_date, end_date = period_input.split()
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        period_map = {
            '1d': timedelta(days=1),
            '5d': timedelta(days=5),
            '1mo': pd.Timedelta(weeks=4),
            '3mo': pd.Timedelta(weeks=12),
            '6mo': pd.Timedelta(weeks=24),
            '1y': pd.Timedelta(weeks=52),
            '2y': pd.Timedelta(weeks=104),
            '5y': pd.Timedelta(weeks=260),
            '10y': pd.Timedelta(weeks=520),
            'since begin of year': datetime.now().replace(month=1, day=1),
            'max': None
        }

        if period_input == 'max':
            start_date = datetime.min
            end_date = datetime.max
        elif period_input in period_map:
            start_date = datetime.now() - period_map[period_input]
            end_date = datetime.now()

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, start_date, end_date)
    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    dd.add_technical_indicators(stock_data)

    dd.calculate_std(stock_data)

    dplt.create_and_save_plot(stock_data, ticker, period_input)

    # Использование собственного стиля
    dplt.create_and_save_plot(stock_data, ticker, period_input, style='custom_style')

    dd.calculate_and_display_average_price(stock_data)

    dd.notify_if_strong_fluctuations(stock_data)

    filename = 'DataF.csv'
    dd.export_data_to_csv(stock_data, filename)


if __name__ == "__main__":
    main()
