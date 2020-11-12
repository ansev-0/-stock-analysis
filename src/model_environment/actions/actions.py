from src.model_environment.states import States
from src.model_environment.actions.basic import BasicActions

class StatesActions(States, BasicActions):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._commision_costs = self.init.commision
        self._action_done = False

    @property
    def commision_costs(self):
        return self._commision_costs

    @property
    def incr_profit(self):
        return self._price_incr * self.n_stocks - self._commision_costs

    def reset(self):
        init_states = super().reset()
        self._commision_costs = self.init.commision
        self._action_done = False
        return init_states

    def step(self):
        if not self._action_done and self.time != 0:
            raise ValueError('any action must be done before step')
        super().step()
        self._action_done = False

    def do_action(self, action, n_stocks=None, frac=None):
        self._action_done = True
        return self._transaction(action, n_stocks, frac)  \
            if action != 'no_action' else self._no_action()

    def n_sales_for_percentage(self, perc):
        return int(perc * self.n_stocks)

    def n_purchases_for_percentage(self, perc):
        return int(perc * self.max_float_purchases)

    def enough_money_to_buy(self, n):
        return n <= self.max_purchases

    def enough_stock_to_sell(self, n):
        return n <= self.n_stocks

    def take_money_out(self, money):
        if money <= self.money:
            self.money -= money
            return self.money

        raise ValueError(f'Not enough money, invest money : {self.money}')


    def _transaction(self, action, n_stocks, frac):
        try:
            self._check_valid_action_parameters(n_stocks, frac)
            return getattr(self, f'_{action}')(n_stocks, frac)

        except Exception as error:
            self._action_done = False
            print(error)
            raise ValueError('Invalid action, You must pass: buy, sell or  no_action')


    def _buy(self, n_stocks=None, frac=None):
        # check if frac_arg
        frac_arg = frac is not None
        #if frac arg calculate n_stocks
        if frac_arg:
            n_stocks = self.n_purchases_for_percentage(frac)

        if (n_stocks > 0) and (frac_arg or self.enough_money_to_buy(n_stocks)):
            if not frac_arg:
                frac = n_stocks // self.max_purchases

            self._commision_costs = self._get_commision_costs(n_stocks)
            self.order_buy(n_stocks)
            return frac, n_stocks, True
        else:
            return self._no_action()


    def _sell(self, n_stocks=None, frac=None):

        frac_arg = frac is not None
        if frac_arg:
            n_stocks = self.n_sales_for_percentage(frac)

        if (n_stocks > 0) and (frac_arg or self.enough_stock_to_sell(n_stocks)):
            if not frac_arg:
                frac = n_stocks // self.n_stocks

            self._commision_costs = self._get_commision_costs(n_stocks)
            self.order_sell(n_stocks)
            return frac, n_stocks, True
        else: 
            return self._no_action()

    def _no_action(self):
        self._commision_costs = 0
        return 0, 0, False

    @staticmethod
    def _check_valid_action_parameters(action, frac):
         if (action and frac) or (action is None and frac is None): 
             raise ValueError('You must pass action or frac parameters')

#from src.train.rl_model.commision.degiro.degiro import CommisionDegiro
#import pandas as pd
#
#commision = CommisionDegiro.from_db(frecuency='daily', date_range=('01/01/2010', '01/01/2012'))
#states_actions = StatesActions((0, 10, 2), (0, 1000, 50), commision, time_serie=pd.Series(range(len(commision.fixed))), done_rule = 'local_min_or_max')
#states_actions.reset()
#states_actions.reset()
#print(
#states_actions.commision.fixed[:7],
#states_actions.commision_costs,
#states_actions.max_purchases,
#states_actions.money,
#states_actions.stock_price,
#'\n',
#'-' * 50,
#'\n',
#states_actions.do_action('buy', n_stocks=1, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('buy', n_stocks=states_actions.max_purchases, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('sell', n_stocks=1, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('sell', n_stocks=states_actions.n_stocks, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#)
#
#states_actions.reset()
#
#print(
#states_actions.commision.fixed[:3],
#states_actions.commision_costs,
#states_actions.max_purchases,
#states_actions.money,
#states_actions.stock_price,
#'\n',
#'-' * 50,
#'\n',
#states_actions.do_action('buy', n_stocks=1, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('buy', n_stocks=states_actions.max_purchases, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('sell', n_stocks=1, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('sell', n_stocks=states_actions.n_stocks, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#'\n',
#'-'*50,
#'\n',
#states_actions.do_action('sell', n_stocks=states_actions.n_stocks, frac=None),
#states_actions.money,
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.step(),
#states_actions.commision_costs,
#states_actions.profit,
#states_actions.incr_profit,
#states_actions.max_float_purchases,
#)
