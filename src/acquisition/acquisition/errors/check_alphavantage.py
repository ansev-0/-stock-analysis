from src.acquisition.acquisition.errors import check_errors
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.mappers import map_dict_from_underscore
from numpy import isin
from pandas import to_datetime

class ErrorsResponseApiAlphavantage(check_errors.ErrorsResponseApi):
    '''
    This class generates exceptions related to the data acquired from the Alphavantage API
    '''
    def __init__(self):
        self._map_test = {'TIME': self._time_series,
                          'GLOBAL': self._stock_time_series_global,
                          'SYMBOL': self._stock_time_series_symbol,
                          'CURRENCY': self._cryptocurrencis,
                          'FX': self._time_series,
                          'DIGITAL': self._time_series,
                          'SECTOR': self._sector_performance,
                          'OVERVIEW' : self._fundamental_data,
                          'BALANCE' : self._fundamental_data,
                          'INCOME' : self._fundamental_data,
                          'CASH' : self._fundamental_data,
                          'EARNINGS' : self._fundamental_data,
                          }


    def pass_test(self, json, query):
        '''

        This function maps the json format test function
        and raises an exception if it returns True.

        '''
        json_keys = list(json)
        if map_dict_from_underscore(dict_to_map=self._map_test,
                                    function=query['function'],
                                    n=0,
                                    default_key='TIME')(json_keys):

            raise AlphaVantageError('json received invalid to type inquiry: {}'
                                    .format(query['function']),
                                    {'query': query, 'json_keys': json_keys})

    def _time_series(self, json_keys):
        return self._not_time_dict(json_keys) & ((len(json_keys) != 2) or (json_keys[0] != 'Meta Data')) 

    @staticmethod
    def _fundamental_data(json_keys):
        return "symbol" not in tuple(map(lambda key: key.lower(), json_keys))

    @staticmethod
    def _stock_time_series_global(json_keys):
        return (json_keys[0] != 'Global Quote') or (len(json_keys) != 1)

    @staticmethod
    def _stock_time_series_symbol(json_keys):
        return (json_keys[0] != 'bestMatches') or (len(json_keys) != 1)

    @staticmethod
    def _cryptocurrencis(json_keys):
        return (json_keys[0] != 'Realtime Currency Exchange Rate') or (len(json_keys) != 1)

    @staticmethod
    def _sector_performance(json_keys):
        return (json_keys[0] != 'Meta Data') or (len(json_keys) != 11)

    @staticmethod
    def _not_time_dict(json_keys):
        try:
            to_datetime(json_keys)
            return False
        except Exception:
            return True






