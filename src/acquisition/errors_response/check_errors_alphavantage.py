from src.acquisition.errors_response import check_errors
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.mappers import map_dict_from_underscore, switch_None

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
                          }


    def pass_test(self, json, query, decoded_function=None):
        '''
        This function maps the json format test function
        and raises an exception if it returns True
        '''
        json_keys = list(json)
        map_function = switch_None(decoded_function, query['function'])
        if map_dict_from_underscore(dict_to_map=self._map_test,
                                    function=map_function,
                                    n=0,
                                    default_key='TIME')(json_keys):

            raise AlphaVantageError('json received invalid to type inquiry: {}'.format(query['function']),
                                    {'query': query, 'json_keys': json_keys})

    def _time_series(self, json_keys):
        return (json_keys[0] != 'Meta Data') or (len(json_keys) != 2)

    def _stock_time_series_global(self, json_keys):
        return (json_keys[0] != 'Global Quote') or (len(json_keys) != 1)

    def _stock_time_series_symbol(self, json_keys):
        return (json_keys[0] != 'bestMatches') or (len(json_keys) != 1)

    def _cryptocurrencis(self, json_keys):
        return (json_keys[0] != 'Realtime Currency Exchange Rate') or (len(json_keys) != 1)

    def _sector_performance(self, json_keys):
        return (json_keys[0] != 'Meta Data') or (len(json_keys) != 11)





