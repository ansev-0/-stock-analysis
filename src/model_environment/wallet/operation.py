import numpy as np

class Operation:
    def __init__(self, purchases={}, sales={}):
        assert isinstance(purchases, dict)
        self._check_valid_amounts(purchases)
        assert isinstance(sales, dict)
        self._check_valid_amounts(sales)
        self.purchases = purchases
        self.sales = sales

    @staticmethod
    def _check_valid_amounts(dict_params):
        if not np.all(np.array(list(dict_params.values())) > 0):
            raise ValueError('Invalid operations, values must be positive')

