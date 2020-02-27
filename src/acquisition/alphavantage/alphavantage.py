import requests
import time
from src import request_api
from src.acquisition.errors_response import check_errors_alphavantage as errors_response
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.builders import inlist
from src.tools.mappers import switch_None

class AlphaVantage:

    _AV_URL = "https://www.alphavantage.co/query?"
    def __init__(self, apikey, delays=None, **kwards):
        self.apikey = apikey
        self.default_params = {'datatype' : 'json',
                               'apikey' : self.apikey}
        self.config(delays)
        self.__check_response = errors_response.ErrorsResponseApiAlphavantage()
        self.request = request_api.RequestsApi(base_url=self._AV_URL, **kwards)

    def config(self, delays = None):
        self.delays = switch_None(delays, [60,20])
        self.attemps = len(self.delays) + 1

    def __read(self, query):
        count_attemps = 0
        while count_attemps < self.attemps:
            try:
                response = self.request.get(params=query)
            except requests.exceptions.RequestException as error:
                return self.__build_tuple_error(query=query,
                                                status_code=response.status_code,
                                                error=error)
            json = response.json()
            count_attemps += 1 #attemp n
            try:
                self.__check_response.pass_test(json, query)
            except AlphaVantageError:
                if count_attemps == self.attemps:
                    return self.__build_tuple_error(query=query,
                                                    status_code=response.status_code,
                                                    error=json.copy())
                    
                #try again
                time.sleep(self.delays[count_attemps-1])
            else:
                #connect successfull, save useful data
                return json

    @classmethod
    def _get_data(cls, func):

        def read_url(self, *args, **kwards):
             func_params = dict(zip(map(str.lower, func.__code__.co_varnames[1:]), func(self, **kwards)))
             query = dict(func_params, **self.default_params)
             return self.__read(query=query)

        return read_url

    @staticmethod
    def __build_tuple_error(query, status_code, error):
        return query, {'status code' : status_code, 'response': error}

