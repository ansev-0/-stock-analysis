
from src.data_preparation.errors.check_datetime_index import CheckDateTimeIndex
import pandas as pd
class DateTimeIndexFeatures:
    def __init__(self, datetimeindex):
        self.check_errors = CheckDateTimeIndex()
        self.check_errors.check_datetime_index(datetimeindex)
        self.datetimeindex = datetimeindex

    def series_diff(self):
        return self.datetimeindex.to_series().diff()

    def check_time_step(self, step):
        return self.series_diff().gt(pd.Timedelta(step))

    def continuos_time_blocks(self, **kwargs):
        return self.check_time_step(**kwargs).cumsum()
