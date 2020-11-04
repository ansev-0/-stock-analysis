from src.train.rl_model.commision.commision import Commision
from src.brokers.database.commision.find import FindCommisionFromBroker

class CommisionDegiro(Commision):

    measurement_units = 'USD'

    def __init__(self, 
                 date_range=None,
                 from_db=True, 
                 fixed=None, 
                 vars=None, 
                 frecuency='daily'):

            self._fixed = None
            self._vars = None
            self._find_commision = FindCommisionFromBroker(frecuency, 'degiro')

            if from_db:
                self._fixed, self._vars = self._find_commision.in_usd(date_range)
            else:
                self._fixed, self._vars = fixed, vars

    @property
    def fixed(self):
        return self._fixed

    @property
    def vars(self):
        return self._vars


    def __call__(self, n_stocks, time=None, *args, **kwargs):
        return self._vars * n_stocks + self._fixed[time] if time is not None\
            else self._vars * n_stocks + self._fixed


commision = CommisionDegiro(date_range=('01/01/2010', '01/01/2012'))
