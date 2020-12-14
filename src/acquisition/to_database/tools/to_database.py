from collections import defaultdict
from pandas import to_datetime
from re import sub

class CreateDictsWithSameId:

    def __init__(self, frecuency):
        self.frecuency = frecuency

    def __call__(self, data):

        '''
        This function adapts the format of the json received from the Alphavantage API
        to the format necessary to update the database using :

        update
        '''

        cumulative_dict = defaultdict(dict)
        for date, values in data.items():
            cumulative_dict[date[:self._return_index_from_frecuency()]]\
                .update({date : {sub(r'^[\d+]. ', '', name) : value
                            for name, value in values.items()}
                         })

        return list(map(lambda items: {'_id' : to_datetime(items[0]),
                                       'data' : items[1]},
                        cumulative_dict.items())
                   )


    def _return_index_from_frecuency(self):

        if self.frecuency == 'intraday':
            return 10
        elif self.frecuency == 'daily':
            return 7

        raise ValueError('Frecuency does not supported')

