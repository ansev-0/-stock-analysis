from src.model_environment.time_states import TimeStatesValues
from src.model_environment.init_state import InitState


class States:

    def __init__(self, init_n_stocks, init_money, commision, time_serie=None, cache_id=None):

        #init
        self._max_float_purchases = None
        self._done = None
        self._stock_price = None
        self._incr_n_stocks = None
        self._n_stocks = None
        self._money = None
        self._historic_profit = []
        self.terminal = None
        self.time = None
        #get commision object
        self.commision = commision
        #get time values
        self.time_states_values = TimeStatesValues(cache_id, time_serie)
        self.reset_time_properties()
        #init state
        self.init = InitState(init_n_stocks, 
                              init_money, 
                              self._stock_price, 
                              self.commision(time=self.time,
                                             n_stocks=init_n_stocks, 
                                             price=self._stock_price)
                            )
        self.reset_money()
        self.reset_n_stocks()
        self._update_max_float_purchases()

        
    @property
    def done(self):
        return self._done

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
    def stock_price(self):
        return self._stock_price

    @property
    def inventory_price(self):
        return self.gross_inventory_price - self._get_commision_costs(self._n_stocks)

    @property
    def gross_inventory_price(self):
        return self._n_stocks * self._stock_price

    @property
    def profit(self):
        return self.inventory_price + self._money - self.init.money - self.init.inventory_price

    def step(self):
        self.time += 1
        self._update_time_vars()
        self._update_max_float_purchases()
        #save profit
        self._historic_profit.append(self.profit)
        
    def reset_n_stocks(self):
        self._incr_n_stocks = 0
        self._n_stocks = self.init.n_stocks

    def reset_money(self):
        self._money = self.init.money

    def reset_time_properties(self):
        self.time = 0
        self._update_time_vars()

    def reset(self): 
        self._historic_profit = []
        self.reset_time_properties()
        self.reset_n_stocks()
        self.reset_money()
        self._update_max_float_purchases()

    def _update_time_vars(self):
        self._stock_price, self._price_incr, self._done = self.time_states_values(self.time)
        self.terminal = self.time == len(self.time_states_values) - 1   

    def _get_commision_costs(self, n_stocks):
        return self.commision(n_stocks=n_stocks, price=self.stock_price, time=self.time)

    def _update_max_float_purchases(self):
        self._max_float_purchases = self.commision.max_purchases(self.time, self._stock_price, self._money)
