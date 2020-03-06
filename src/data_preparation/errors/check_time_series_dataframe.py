import pandas as pd
class CheckSplitDataFrame:

    @staticmethod
    def check_datetime_index(index):
        if not isinstance(index, pd.DatetimeIndex):
            raise TypeError('The index must be instance of pd.DatetimeIndex')
        
    @staticmethod
    def check_valid_format_output(format_output):
        if format_output not in [list, dict]:
            raise TypeError('format output must be instance of dict or list')