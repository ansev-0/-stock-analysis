from src.train.rl_model.commision.commision import Commision
from src.brokers.database.commision.find import FindCommisionFromBroker
from src.train.rl_model.commision.decode_commision_cache import DecodeCommisionCache

class CommisionDegiro(Commision):

    measurement_units = 'USD'

    def __init__(self, fixed=None, variables=None, **kwargs):
        self._fixed = fixed
        self._vars = variables

    @property
    def fixed(self):
        return self._fixed

    @property
    def vars(self):
        return self._vars


    @classmethod
    def from_db(cls, frecuency, date_range):
        return cls(*FindCommisionFromBroker(frecuency, 'degiro').in_usd(date_range))


    @classmethod
    def from_cache_train(cls, dict_cache):
        return cls(*DecodeCommisionCache(('fixed', 'variables'))(dict_cache))
        

    def __call__(self, n_stocks, time=None, *args, **kwargs):
        return self._vars * n_stocks + self._fixed[time] if n_stocks > 0 else 0 