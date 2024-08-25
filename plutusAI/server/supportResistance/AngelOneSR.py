import pandas as pd
from datetime import datetime, timedelta
import logging

from plutusAI.models import IndexDetails
from plutusAI.server.base import getCurrentIndexValue
from plutusAI.server.broker.Broker import Broker
from plutusAI.server.constants import *

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("support_resistance.log"), logging.StreamHandler()]
)


class SupportResistanceCalculator:
    INDEX_SYMBOL_MAP = {
        NIFTY_50: "nifty",
        NIFTY_BANK: "bank_nifty",
        NIFTY_FIN_SERVICE: "fin_nifty"
    }

    def __init__(self, email, index_symbol,threshold):
        self.broker = Broker(email, index_symbol).BrokerObject
        self.index_symbol = index_symbol
        self.index_symbol_internal = self.INDEX_SYMBOL_MAP.get(index_symbol, None)
        self.threshold=threshold

    def remove_nearby_levels(self,levels):

        if not levels:
            return []

        # Sort levels in ascending order
        levels = sorted(levels)

        filtered_levels = [levels[0]]  # Initialize with the first level

        # Iterate through the sorted list starting from the second element
        for i in range(1, len(levels)):
            # Check if the difference between the current level and the last added level is greater than or equal to the threshold
            if levels[i] - filtered_levels[-1] >= self.threshold:
                filtered_levels.append(levels[i])

        return filtered_levels

    def is_support(self, df, index, n1, n2):
        """
        Determine if a point is a support level.
        """
        for i in range(index - n1 + 1, index + 1):
            if df.low[i] > df.low[i - 1]:
                return False
        for i in range(index + 1, index + n2 + 1):
            if df.low[i] < df.low[i - 1]:
                return False
        return True

    def is_resistance(self, df, index, n1, n2):
        """
        Determine if a point is a resistance level.
        """
        for i in range(index - n1 + 1, index + 1):
            if df.high[i] < df.high[i - 1]:
                return False
        for i in range(index + 1, index + n2 + 1):
            if df.high[i] > df.high[i - 1]:
                return False
        return True

    def calculate_support_resistance(self, data):
        try:
            final_support_resistance = []
            index_last_price = getCurrentIndexValue("nifty")
            sr = []
            n1 = 3
            n2 = 1
            for row in range(3, len(data.index) - 2):  # len(df)-n2
                if self.is_support(data, row, n1, n2):
                    sr.append((row, data.low[row], 1))
                if self.is_resistance(data, row, n1, n2):
                    sr.append((row, data.high[row], 2))

            plotlist1 = [float(x[1]) for x in sr if x[2] == 1]  # support
            plotlist2 = [float(x[1]) for x in sr if x[2] == 2]  # resistance
            plotlist1.sort()
            plotlist2.sort()

            check = 0
            if self.index_symbol == NIFTY_50:
                check = 50
            elif self.index_symbol == NIFTY_FIN_SERVICE:
                check = 50
            elif self.index_symbol == NIFTY_BANK:
                check = 100

            i = 1
            while i < len(plotlist1):
                if abs(plotlist1[i] - plotlist1[i - 1]) <= check:
                    plotlist1.pop(i)
                else:
                    i += 1

            i = 1
            while i < len(plotlist2):
                if abs(plotlist2[i] - plotlist2[i - 1]) <= check:
                    plotlist2.pop(i)
                else:
                    i += 1

            for value in plotlist1:
                if value <= index_last_price:
                    final_support_resistance.append(value)

            for value in plotlist2:
                if value >= index_last_price:
                    final_support_resistance.append(value)
            print(final_support_resistance)
            final_support_resistance = self.remove_nearby_levels(final_support_resistance)
            print(f"{self.index_symbol} levels == {final_support_resistance}")

            return final_support_resistance

        except Exception as e:
            print(e)

    def get_date_range(self, days=30):
        """
        Get the date range for the past 'days' days, where the start date is the start of the day
        and the end date is the end of the day, both formatted as 'YYYY-MM-DD HH:MM'.
        """
        today = datetime.now()  # Get the current date and time
        end_date = today - timedelta(days=1)  # Calculate yesterday's date
        start_date = end_date - timedelta(days=days)  # Calculate the start date by subtracting 'days' from the end date

        # Set the time to the start of the start_date (00:00) and end of the end_date (23:59)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Format both dates to include date and time as 'YYYY-MM-DD HH:MM'
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M')

        return start_date_str, end_date_str  # Return the formatted start and end dates

    def fetch_support_resistance(self, instrument_name, timeframe, days=30):
        """
        Fetch historical data and calculate support/resistance levels.
        """
        try:
            from_date, to_date = self.get_date_range(days)
            print(f"Fetching data for {self.index_symbol} from {from_date} to {to_date} in {timeframe} timeframe.")

            historical_data = pd.DataFrame(
                self.broker.getCandleData("NSE", self.broker.getTokenForSymbol(instrument_name), from_date, to_date,timeframe)
            )
            print(historical_data)
            return self.calculate_support_resistance(historical_data)

        except Exception as e:
            print(f"Error fetching support/resistance for {self.index_symbol}: {e}")
            return [], []
