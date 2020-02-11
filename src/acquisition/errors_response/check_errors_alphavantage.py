from src.acquisition.errors_response import check_errors
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.mappers import map_dict_from_underscore,switch_None

class ErrorsResponseApiAlphavantage(check_errors.ErrorsResponseApi):

    def __init__(self):
        self._map_test = {'TIME':self._TimeSeries,
                          'GLOBAL':self._StockTimeSeries_global,
                          'SYMBOL':self._StockTimeSeries_symbol,
                          'CURRENCY':self._Cryptocurrencis,
                          'FX': self._TimeSeries,
                          'DIGITAL':self._TimeSeries,
                          'SECTOR':self._SectorPerformance,
                          }
        
    def pass_test(self,json,query,decoded_function = None):

        json_keys = list(json)
        map_function  = switch_None(decoded_function,query['function'])

        if map_dict_from_underscore(dict_to_map = self._map_test,
                                    function = map_function,
                                    n=0,
                                    default_key = 'TIME')(json_keys):

            raise AlphaVantageError('json received invalid to type inquiry: {}'.format(query['function']),
                                    {'query':query,'json_keys':json_keys})
                                    

    def _TimeSeries(self,json_keys): return (json_keys[0]!= 'Meta Data') or (len(json_keys)!=2)
            

    def _StockTimeSeries_global(self,json_keys): return (json_keys[0]!='Global Quote') or (len(json_keys)!=1)
        

    def _StockTimeSeries_symbol(self,json_keys): return (json_keys[0]!='bestMatches') or (len(json_keys)!=1)
        

    def _Cryptocurrencis(self,json_keys): return (json_keys[0]!='Realtime Currency Exchange Rate') or (len(json_keys)!=1)
        

    def _SectorPerformance(self,json_keys): return (json_keys[0]!= 'Meta Data') or (len(json_keys)!=11)