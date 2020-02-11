from acquisition.errors_response import check_errors

class ErrorsResponseApi_Alphavantage(check_errors.ErrorsResponseApi):

    def __init_(self):

        self._map_test = {'TIME':self._TimeSeries,
                          'GLOBAL':self._StockTimeSeries_global,
                          'SYMBOL':self._StockTimeSeries_symbol,
                          'CURRENCY':self._Cryptocurrencis,
                          'FX': self._TimeSeries,
                          'DIGITAL':self._TimeSeries,
                          'SECTOR':self._SectorPerformance,
                          }
        

    def pass_test(self,json,query):
        
        key_map = query['function'].split('_')[0]
        try:
           invalid_response = self._map_test[key_map](json)
        except KeyError:
            invalid_response = self._TimeSeries(json)
        finally:
            if invalid_response: raise ValueError('Invalid data response')

    def _TimeSeries(self,json):
        return (list(json)[0]!= 'Meta Data') or (len(json)!=2)
            

    def _StockTimeSeries_global(self,json):
        return (list(json)[0]!='Global Quote') or (len(json)!=1)
        

    def _StockTimeSeries_symbol(self,json):
        return (list(json)[0]!='bestMatches') or (len(json)!=1)
        

    def _Cryptocurrencis(self,json):
        return (list(json)[0]!='Realtime Currency Exchange Rate') or (len(json)!=1)
        

    def _SectorPerformance(self,json):
        return (list(json)[0]!= 'Meta Data') or (len(json)!=11)