import pandas as pd

def calculate_and_display_average_price(data):
    data = data['Close'].mean()
    print(f"Средняя цена закрытия акций за период: {data}")


