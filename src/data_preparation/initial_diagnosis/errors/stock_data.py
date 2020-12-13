import pandas as pd
import numpy as np
from src.exceptions.process_exceptions import DataSelectionProcessError


class CheckStockDataDiagnosis:

    @staticmethod
    def check_is_frame(frame):
        if not isinstance(frame, pd.DataFrame):
            raise DataSelectionProcessError('You must pass a DataFrame', TypeError)

    @staticmethod
    def check_datetime_index(index):
        if not isinstance(index, pd.DatetimeIndex):
            raise DataSelectionProcessError('You must pass a DataFrame with DatetimeIndex', TypeError)


    @staticmethod
    def check_columns(columns):

        if isinstance(columns, pd.MultiIndex):
            columns = columns.get_level_values(0)

        if not np.isin(['open','high','low','close'], columns).all():
            raise DataSelectionProcessError('You must pass a DataFrame\
                 with open, high, low, and close columns', ValueError)

class CheckManyStockDataDiagnosis:

    @staticmethod
    def check_columns(columns):
        if not isinstance(columns, pd.MultiIndex):
            raise DataSelectionProcessError('You must pass a MultiIndex\
                 DataFrame with open, high, low, and close in level 0', ValueError)