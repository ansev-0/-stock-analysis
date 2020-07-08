from functools import wraps
import time
import requests
from src.acquisition.acquisition.reader import Reader
from src.acquisition.acquisition.last10k.apikey import ApiKey
from src.tools.mappers import switch_none
from src.view.acquisition.acquisition.status_api import ApiShowStatus 
from src.exceptions.acquisition_exceptions import Last10kError

class Last10K:

    '''
    This class is used to get data from
    https://dev.last10k.com/

    '''
    _LAST_10K_URL = 'https://services.last10k.com/v1/company/'

    def __init__(self, apikey, delays=None, **kwargs):
        self.apikey = apikey
        self.config(delays)
        self.show_status = ApiShowStatus()
        self._reader = Reader(**kwargs)

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
            self.show_status.notify_try_connect('Last10k')
            response = self._reader.read(query, auth=ApiKey(self.apikey))

            status_code = response.status_code

            if not status_code == requests.codes.ok:
                error_response = response
            else: 
                self.show_status.notify_json_received_succesfully()
                return response.json()
        else:
            return self.__build_tuple_error(query=query,
                                                status_code=status_code,
                                                error=error_response)

    @classmethod
    def _get_data(cls, func):

        @wraps(func)
        def read_url(self, company, *args, **kwargs):

            params = func(self, *args, **kwargs)
            query={}

            if isinstance(params, tuple):
                self._reader.base_url = self._LAST_10K_URL + '/'.join([company, params[0]])
                query = params[1]

            elif isinstance(params, str):
                self._reader.base_url = self._LAST_10K_URL + '/'.join([company, params])

            elif not params:
                self._reader.base_url = self._LAST_10K_URL + company

            elif isinstance(params, dict):
                self._reader.base_url = self._LAST_10K_URL + company
                query = params
            else:
                raise Last10kError('Unsupported parameter format', ValueError)

            return self.__read(query=query)
            

        return read_url


    @staticmethod
    def __build_tuple_error(query, status_code, error):
        return query, {'status code' : status_code, 'response': error}
