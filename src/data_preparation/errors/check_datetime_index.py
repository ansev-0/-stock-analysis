import pandas as pd
class CheckDateTimeIndex:
    def check_datetime_index(self, index):
        if not isinstance(index, pd.DatetimeIndex):
            raise TypeError('The index must be instance of pd.DatetimeIndex')