from src.train.rl_model.commision.commision import Commision
from src.brokers.database.commision.find import FindCommisionFromBroker

class CommisionDegiro(Commision):

    measurement_units = 'USD'
    _find_commision = FindCommisionFromBroker('degiro')

    def __init__(self, from_db=True, date_range=None, fixed=None, variables=None):

            self._fixed, self._variables = self._find_commision.in_usd(date_range) \
                if from_db else fixed, variables

    @property
    def fixed(self):
        return self._fixed

    @property
    def variables(self):
        return self._variables


    def __call__(self, n_stocks, time):
        return self._variables * n_stocks + self._fixed[time]


