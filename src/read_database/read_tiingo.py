#from src.database.database import DataBaseAdminDataReader
#from src.read_database.reader_time_series import TimeSeriesDataFromDataBase
from src.read_database.reader import ReaderDataBase
from src.tools.reduce_tools import combine_dicts
import pandas as pd

class ReadTiingoDataFrame(ReaderDataBase):

    def __init__(self):
        super().__init__('tiingo_news','frame')

    def __call__(self, data, start, end, **kwargs):
        output = list(self._get_dict_from_database(data, start, end, **kwargs))
        return self._to_frame(output) if output else output

    def _to_frame(self, list_output):
        return pd.DataFrame([dict_data for d in list_output for key, dict_data in d.items() if key != '_id'])\
                 .set_index('crawl_date').sort_index()





