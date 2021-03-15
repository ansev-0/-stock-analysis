from functools import wraps
import time
from src.acquisition.acquisition.readers.alphavantage_reader import AlphavantageReader
from src.acquisition.acquisition.errors.check_alphavantage import ErrorsResponseApiAlphavantage
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.mappers import switch_none
from src.view.acquisition.acquisition.status_api import ApiShowStatus

class AlphaVantage:

    '''
    This class is used to get data from
    https://www.alphavantage.co/

    '''

    _AV_URL = "https://www.alphavantage.co/query?"
    
    def __init__(self, apikey, delays=None, **kwargs):
        self.apikey = apikey
        self.config(delays)
        self.__check_response = ErrorsResponseApiAlphavantage()
        self._reader = AlphavantageReader(base_url=self._AV_URL, **kwargs)
        self.show_status = ApiShowStatus()

    @property
    def default_params(self):
        return {
                #'datatype' : 'json',
                'apikey' : self.apikey
                }

    def config(self, delays=None):
        self.delays = switch_none(delays, [60, 20])
        self.attemps = len(self.delays) + 1

    def __read(self, query):
        count_attemps = 0
        while count_attemps < self.attemps:
            error_response = None
            status_code = None

            if count_attemps != 0:
                #try again
                delay = self.delays[count_attemps-1]
                self.show_status.notify_sleeping(delay)
                time.sleep(delay)

            count_attemps += 1 #attemp n
            self.show_status.notify_try_connect('Alphavantage')
            response = self._reader(query)

            if not isinstance(response, dict):
                error_response = response
            else: 
                
                try:
                    self.__check_response.pass_test(response, query)
                except AlphaVantageError as error:
                    self.show_status.notify_error_format(error)
                    error_response = error
                else:
                    #connect successful, save useful data
                    self.show_status.notify_json_received_succesfully()
                    return response
        else:
            return query, str(error_response)

    @classmethod
    def _get_data(cls, func):

        @wraps(func)
        def read_url(self, *args, **kwargs):
            func_params = dict(zip(map(str.lower, func.__code__.co_varnames[1:]),
                                   func(self, **kwargs)))
            query = dict(func_params, **self.default_params)
            return self.__read(query=query)

        return read_url



