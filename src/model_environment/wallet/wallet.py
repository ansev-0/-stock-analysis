from collections import defaultdict
import numpy as np
import copy

class Wallet:
    
    def __init__(self, stocks : dict, money : float):
        assert isinstance(stocks, dict)
        self._money = None
        self._stocks = defaultdict(int)
        self.update_stocks(stocks)
        self.money = money

    def __str__(self):
        money = f'Money : {self.money}\n'
        if self._stocks:
            return  money + '\n'.join([f'{name_stock} : {amount} uds' 
                                       for name_stock, amount in self._stocks.items()]) 
        return money + 'No stocks in wallet'
        
    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        self._money = np.float32(money)
        if self._money < 0:
            raise ValueError('Money can not be negative')

    @property
    def stocks(self):
        return dict(self._stocks)

    def update_stocks(self, dict_to_update):
        self._stocks.update(dict_to_update)
        assert np.all(np.array(list(self._stocks.values())) >= 0)

    def remove_stock(self, stock, amount):
        assert amount > 0
        self._stocks[stock] -= amount
        assert self._stocks[stock] >= 0

    def add_stock(self, stock, amount):
        assert amount > 0
        self._stocks[stock] += amount

    def copy(self):
        return copy.deepcopy(self)
