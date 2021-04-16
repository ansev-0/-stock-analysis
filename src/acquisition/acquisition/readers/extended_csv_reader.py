from pandas import read_csv
from src.acquisition.acquisition.readers.reader import Reader

class ReaderExtendedCSV(Reader):

    def __init__(self, base_url):
        self._base_url = base_url
        

    @property
    def base_url(self):
        return self._base_url


    def __call__(self, query):
        
        try:
            response = read_csv(self._url(query), index_col='time')\
                .astype(str).to_dict('index')
            
        except Exception as error:
            self._show_status.notify_error()
            return error

        else:
            self._show_status.notify_not_error()
            return response

    def _encode_dict_params(self, dict_params):
        return '&'.join(['='.join((key, str(value))) for key, value in dict_params.items()])

    def _url(self, dict_params):
        return self._base_url + self._encode_dict_params(dict_params)

