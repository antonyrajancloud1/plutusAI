import datetime
import time
import pandas as pd

from plutusAI.models import CandleData


class OHLCDataProcessor:
    def __init__(self):
        self.data_dict = {}
        self.candlestick_data = pd.DataFrame(columns=['timestamp', 'token', 'open', 'high', 'low', 'close'])
        self.start_time = self.get_next_minute_start()


    @staticmethod
    def get_next_minute_start():
        now = datetime.datetime.now()
        next_minute_start = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        if now.second >= 59:  # Adjust the starting point based on your requirement (e.g., start from the current minute if second is 30 or more)
            next_minute_start += datetime.timedelta(minutes=1)
        return next_minute_start

    def format_time(current_time):
        return current_time.strftime('%H:%M:%S')

    def update_candle_data(self,value):
        ltp_values = []
        start_time = self.get_next_minute_start()
        ltp = float(value)
        ltp_values.append(ltp)
        print(ltp_values)
        if datetime.datetime.now() >= start_time + datetime.timedelta(seconds=60):
            open_price = ltp_values[0]
            high_price = max(ltp_values)
            low_price = min(ltp_values)
            close_price = ltp_values[-1]
            print(
                f"{self.format_time(start_time)} - Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")
            new_data = pd.DataFrame({
                'timestamp': [start_time],
                'open': [open_price],
                'high': [high_price],
                'low': [low_price],
                'close': [close_price]
            })
            self.candlestick_data
            self.candlestick_data = pd.concat([self.candlestick_data, new_data], ignore_index=True)
            ltp_values = []
            start_time = self.get_next_minute_start()
