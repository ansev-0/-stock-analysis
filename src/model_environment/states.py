from src.train.database.cache.agents.find import FindAgentTrainCache
import pandas as pd
import numpy as np


class InitState:

    def __init__(self,  init_n_stocks, init_money, init_stock_price, commision):

        self.n_stocks = init_n_stocks
        self.money = init_money
        self.commision = commision
        self.stock_price = init_stock_price
        self._gross_inventory_price = self._get_gross_inventory_price()
        self._inventory_price = self._get_inventory_price()


    @property
    def gross_inventory_price(self):
        return self._gross_inventory_price

    @property
    def inventory_price(self):
        return self._inventory_price

    def _get_gross_inventory_price(self):
        return self.n_stocks * self.stock_price

    def _get_inventory_price(self):
        return self.n_stocks * (self.stock_price - self.commision)

        

class States:

    def __init__(self, init_n_stocks, init_money, commision, time_serie=None, id_cache=None):

        self._historic_profit = []
        self.terminal = False
        self._id_cache = id_cache
        self._time_serie = self._init_time_serie(time_serie).values
        self._time_serie_diff = self._time_serie.diff().values
        self.time = 0
        self._stock_price = self._time_serie[self.time]
        self.init = InitState(init_n_stocks, init_money, self._stock_price, commision)
        self._incr_n_stocks = None
        self._n_stocks = self.init.n_stocks
        self.money = self.init.money
        self.commision = commision

    @property
    def n_stocks(self):
        return self._n_stocks

    @n_stocks.setter
    def n_stocks(self, n_stocks):
        self._incr_n_stocks = n_stocks - self._n_stocks
        self._n_stocks = n_stocks
        
    @property
    def historic_profit(self):
        return self._historic_profit

    @property
    def id_cache(self):
        return self._id_cache

    @property
    def time_serie(self):
        return self._time_serie

    @time_serie.setter
    def time_serie(self, time_serie):
        self._time_serie = time_serie
        self.reset_time()

    @property
    def stock_price(self):
        return self._stock_price

    @property
    def inventory_price(self):
        return self.n_stocks * (self.stock_price - self.commision)

    @property
    def gross_inventory_price(self):
        return self.n_stocks * self.stock_price

    @property
    def profit(self):
        return self.inventory_price + self.money - self.init.money - self.init.inventory_price

    @property
    def incr_profit(self):
        return self._time_serie_diff[self.time] * self.n_stocks \
             - self.commision * self._incr_n_stocks * (1 + np.sign(self._incr_n_stocks))

    @property     
    def inventory_empty(self):
        return self.n_stocks > 0

    def step(self):
        self.time += 1
        self._stock_price = self.time_serie[self.time]
        self.terminal = self.time == len(self.time_serie) - 1
        #save profit
        self._historic_profit.append(self.profit)
        
    def reset_n_stocks(self):
        self._incr_n_stocks = None
        self._n_stocks = self.init.n_stocks

    def reset_money(self):
        self.money = self.init.money

    def reset_time(self):
        self.time = 0
        self._stock_price = self.init.stock_price

    def reset(self):
        self.terminal = False
        self._historic_profit = []
        self.reset_time()
        self.reset_money()
        self.reset_n_stocks()
        

    def _init_time_serie(self, time_serie):

        if self._id_cache is not None:
            return pd.Series(FindAgentTrainCache().\
                find_by_id(self._id_cache, 
                           projection = {'time_values' : True,
                                         '_id' : False})['time_values'])[:-1]
        elif time_serie is not None:
            return time_serie

        raise ValueError('You must pass time_series or id_cache parameters')
    


