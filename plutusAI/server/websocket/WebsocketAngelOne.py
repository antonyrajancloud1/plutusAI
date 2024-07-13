import datetime
import random
import time
import pandas as pd

# Function to get the next minute's start time
def get_next_minute_start():
    now = datetime.datetime.now()
    next_minute_start = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
    if now.second >= 59:  # Adjust based on your requirement
        next_minute_start += datetime.timedelta(minutes=1)
    return next_minute_start

# Function to format time in HH:MM:SS
def format_time(current_time):
    return current_time.strftime('%H:%M:%S')

# Initialize data structures
tokens = ['52000']
candlestick_data_dict = {token: pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close']) for token in tokens}
ltp_values_dict = {token: [] for token in tokens}
start_time_dict = {token: get_next_minute_start() for token in tokens}

# Main loop
try:
    while True:
        for token in tokens:
            # Simulating live data stream (replace this with your actual data retrieval logic)
            ltp = random.randint(int(token), int(token) + 500)
            ltp_values_dict[token].append(ltp)

            # Check if 60 seconds have passed for the specific token
            if datetime.datetime.now() >= start_time_dict[token] + datetime.timedelta(seconds=60):
                open_price = ltp_values_dict[token][0]
                high_price = max(ltp_values_dict[token])
                low_price = min(ltp_values_dict[token])
                close_price = ltp_values_dict[token][-1]

                # Print OHLC values and current time
                print(f"{format_time(start_time_dict[token])} - Token: {token}, Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}")

                # Add new row of data
                new_data = pd.DataFrame({
                    'timestamp': [start_time_dict[token]],
                    'open': [open_price],
                    'high': [high_price],
                    'low': [low_price],
                    'close': [close_price]
                })

                # Check if new_data is not empty or all-NA before concatenating
                if not new_data.isna().all().all():
                    candlestick_data_dict[token] = pd.concat([candlestick_data_dict[token], new_data], ignore_index=True)

                # Reset for next interval
                ltp_values_dict[token] = []
                start_time_dict[token] = get_next_minute_start()

        # Wait for the next iteration
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Process interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
