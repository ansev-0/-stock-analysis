from src.acquisition.acquisition.readers.requests_reader import  RequestsReader
from src.acquisition.acquisition.readers.extended_csv_reader import  ReaderExtendedCSV


class AlphavantageReader(RequestsReader):

    def __init__(self, base_url='', **kwargs):
        
        super().__init__(base_url, **kwargs)
        self._extended_reader = ReaderExtendedCSV(base_url)

    def __call__(self, query, **kwargs):
        return self._extended_reader(query) if query['function'] == 'TIME_SERIES_INTRADAY_EXTENDED' \
            else super().__call__(query, **kwargs)