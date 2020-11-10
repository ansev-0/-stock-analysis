from src.train.database.cache.agents.find import FindAgentTrainCache
from src.model_environment.init_state import InitState
import pandas as pd
import numpy as np



class States:

    def __init__(self, init_n_stocks, init_money, commision, time_serie=None, id_cache=None):

        self.time = 0
        self._historic_profit = []
        self.terminal = False
        self._id_cache = id_cache
        #get commision object
        self.commision = commision
        #get time series
        self._pandas_time_serie = self._init_time_serie(time_serie)
        self._time_serie = self._pandas_time_serie.values
        self._time_serie_diff = self._pandas_time_serie.diff().values
        #get stock price
        self._stock_price = self._time_serie[self.time]
        #init state
        self.init = InitState(init_n_stocks, 
                              init_money, 
                              self._stock_price, 
                              self.commision(time=self.time,
                                             n_stocks=init_n_stocks, 
                                             price=self._stock_price)
                            )
        self._incr_n_stocks = 0
        self._n_stocks = self.init.n_stocks
        self._money = self.init.money
        self._max_float_purchases = self._get_max_float_purchases()
        self._done = self._get_serie_done()
        
    @property
    def done(self):
        return self._done[self.time]

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        self._money = money

    @property
    def n_stocks(self):
        return self._n_stocks

    @n_stocks.setter
    def n_stocks(self, n_stocks):
        self._incr_n_stocks = n_stocks - self._n_stocks
        self._n_stocks = n_stocks

    @property
    def max_sales(self):
        return self._n_stocks

    @property
    def max_float_purchases(self):
        return self._max_float_purchases

    @property
    def max_purchases(self):
        return int(self._max_float_purchases)

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
        return self.gross_inventory_price - self._get_commision_costs(self.n_stocks)

    @property
    def gross_inventory_price(self):
        return self.n_stocks * self.stock_price

    @property
    def profit(self):
        return self.inventory_price + self._money - self.init.money - self.init.inventory_price

    @property     
    def inventory_empty(self):
        return self.n_stocks > 0


    def step(self):

        self.time += 1
        self._stock_price = self.time_serie[self.time]
        self.terminal = self.time == len(self.time_serie) - 1
        #save profit
        self._historic_profit.append(self.profit)
        #update max purchases
        self._max_float_purchases = self._get_max_float_purchases()
        
    def reset_n_stocks(self):
        self._incr_n_stocks = 0
        self._n_stocks = self.init.n_stocks

    def reset_money(self):
        self._money = self.init.money

    def reset_time(self):
        self.time = 0
        self._stock_price = self.init.stock_price

    def reset(self): 

        self.terminal = False
        self._historic_profit = []
        self.reset_time()
        self.reset_money()
        self.reset_n_stocks()
        self._max_float_purchases = self._get_max_float_purchases()

    def _get_commision_costs(self, n_stocks):
        return self.commision(n_stocks=n_stocks, price=self.stock_price, time=self.time)


    def _get_max_float_purchases(self):
        self.commision.fixed[self.time]
        return (self._money - self.commision.fixed[self.time]) / (self.stock_price + self.commision.vars)

        
    def _init_time_serie(self, time_serie):

        if self._id_cache is not None:
            return pd.Series(FindAgentTrainCache().\
                find_by_id(self._id_cache, 
                           projection = {'time_values' : True,
                                         '_id' : False})['time_values'])[:-1]
        elif time_serie is not None:
            return time_serie

        raise ValueError('You must pass time_series or id_cache parameters')


    def _get_serie_done(self):
        return (self._pandas_time_serie.lt(self._pandas_time_serie.shift())
            & self._pandas_time_serie.lt(self._pandas_time_serie.shift(-1))).values
    