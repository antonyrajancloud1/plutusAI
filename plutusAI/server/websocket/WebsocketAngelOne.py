import datetime
import time
import pandas as pd

from plutusAI.models import CandleData


class OHLCDataProcessor:
    def __init__(self):
        self.data_dict = {}
        self.ohlc_data = pd.DataFrame(columns=['timestamp', 'token', 'open', 'high', 'low', 'close'])
        self.start_time = self.get_next_minute_start()

    @staticmethod
    def get_next_minute_start():
        """Get the next minute's start time."""
        now = datetime.datetime.now()
        next_minute_start = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        if now.second >= 0:
            next_minute_start += datetime.timedelta(minutes=1)
        return next_minute_start

    def update_data(self, token, ltp):
        """Update data with new token and LTP value."""
        if datetime.datetime.now() >= self.start_time:
            if token not in self.data_dict:
                self.data_dict[token] = []
            self.data_dict[token].append(float(ltp))
            print(self.data_dict)
            self.construct_ohlc_data()

    def construct_ohlc_data(self):
        """Construct OHLC data at the start of every minute."""
        if datetime.datetime.now() >= self.start_time:
            for token, ltp_values in self.data_dict.items():
                if ltp_values:
                    open_price = ltp_values[0]
                    high_price = max(ltp_values)
                    low_price = min(ltp_values)
                    close_price = ltp_values[-1]

                    # Append new OHLC data
                    new_data = pd.DataFrame({
                        'timestamp': [self.start_time],
                        'token': [token],
                        'open': [open_price],
                        'high': [high_price],
                        'low': [low_price],
                        'close': [close_price]
                    })
                    self.ohlc_data = pd.concat([self.ohlc_data, new_data], ignore_index=True)
                    CandleData.objects.create(**new_data)
            # Reset for next interval
            self.data_dict = {token: [] for token in self.data_dict.keys()}
            self.start_time = self.get_next_minute_start()

    def get_ohlc_data(self):
        """Get the OHLC data DataFrame."""
        return self.ohlc_data

#
# # Usage example
# processor = OHLCDataProcessor()
#
# # Simulating data updates every second
# try:
#     while True:
#         # Example data update
#         processor.update_data('99926000', '24502.15')
#         processor.update_data('99926000', '24503.15')
#         processor.update_data('99926000', '24500.15')
#         processor.update_data('99926000', '24505.15')
#         processor.update_data('99926002', '24500.15')
#         processor.update_data('99926002', '24505.15')
#         # Sleep for a while to simulate real-time data
#         time.sleep(1)
#
#         # Print the OHLC data
#         print(processor.get_ohlc_data())
# except KeyboardInterrupt:
#     print("Process interrupted by user.")
# except Exception as e:
#     print(f"An error occurred: {e}")
