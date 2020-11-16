import numpy as np

class ValueOrRandomRange:
    
    def __init__(self, data):
        self._arg_data = data
        self._data = data
        self._update_data_func = self._random_choice_data \
            if isinstance(data, tuple) or isinstance(data, list) else lambda *args: None
            
    def _random_choice_data(self):
        self._data= np.random.choice(range(*self._arg_data))
     
    @property
    def data(self):
        self._update_data_func()
        return self._data


class InitState:

    def __init__(self,  
                 init_n_stocks, 
                 init_money, 
                 init_stock_price, 
                 commision_func):

        self._n_stocks = None
        self._money = None
        self._gross_inventory_price = None
        self._inventory_price = None

        self.stock_price = init_stock_price
        self._n_stocks_get = ValueOrRandomRange(init_n_stocks)
        self._money_get = ValueOrRandomRange(init_money)
        self._commision_func = commision_func


    @property
    def commision(self):
        return self._commision_func(self._n_stocks)

    @property
    def n_stocks(self):
        self._n_stocks = self._n_stocks_get.data
        self._gross_inventory_price = self._get_gross_inventory_price()
        self._inventory_price = self._get_inventory_price()
        
        return self._n_stocks

    @property
    def money(self):
        self._money = self._money_get.data
        return self._money

    @property
    def gross_inventory_price(self):
        return self._gross_inventory_price

    @property
    def inventory_price(self):
        return self._inventory_price

    def _get_gross_inventory_price(self):
        return self._n_stocks * self.stock_price

    def _get_inventory_price(self):
        return self.gross_inventory_price - self.commision
