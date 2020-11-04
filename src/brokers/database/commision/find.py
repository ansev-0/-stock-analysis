from src.brokers.database.find import FindBrokers
from src.read_database.forex_data import ForexDataFromDataBase

class FindCommisionFromBroker(FindBrokers):
    
    def __init__(self, frecuency, *args, **kwargs):
         self._reader_exchange = ForexDataFromDataBase(db_name=f'forex_data_{frecuency}')
         super().__init__(*args, **kwargs)

    def in_usd(self, date_range):

        commisions = self.find_one({'_id' : 'commision'},
                                    projection={'_id' : 0})

        return self._commisions_to_coin('USD', commisions, date_range)

    def _commisions_to_coin(self, coin, commisions, date_range):

        start, end = date_range

        for commision in commisions.values():
            if commision['units'] != coin:
                commision['value'] *= self._reader_exchange.get(start=start, 
                                                                end=end, 
                                                                from_symbol=commision['units'], 
                                                                to_symbol=coin)['close']

        return commisions['fixed']['value'], commisions['variables']['value']
