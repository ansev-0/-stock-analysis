
from src.model_environment.states import States




class StatesActions(States):


    def do_action(self, action, n_stocks=None, frac=None):
        return self._transaction(action, n_stocks, frac)  if action != 'no_action' else self._no_action()

    @property
    def max_purchases(self):
        return int(self._max_float_purchases())

    @property
    def max_sales(self):
        return self.n_stocks

    def n_sales_for_percentage(self, perc):
        return int(perc * self.n_stocks)

    def n_purchases_for_percentage(self, perc):
        return int (self._max_float_purchases() * perc)

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

            return (frac, *self._order_buy(n_stocks))

        else:
            return self._no_action()


    def _order_buy(self, n_stocks):

        self.n_stocks += n_stocks
        income = - 1 * n_stocks * (self.stock_price + self.commision)
        self.money += income
        return n_stocks, True, income


    def _sell(self, n_stocks=None, frac=None):

        frac_arg = frac is not None
        if frac_arg:
            n_stocks = self.n_sales_for_percentage(frac)


        if (n_stocks > 0) and (frac_arg or self.enough_stock_to_sell(n_stocks)):

            if not frac_arg:
                frac = n_stocks // self.max_sales

            return (frac, *self._order_sell(n_stocks))
        else: 
             return self._no_action()

    def _order_sell(self, n_stocks):
        self.n_stocks -= n_stocks
        income = n_stocks * (self.stock_price - self.commision)
        self.money += income
        return n_stocks, True, income


    def _no_action(self):
        return 0, 0, False, 0

    def _max_float_purchases(self):
        return self.money / (self.stock_price + self.commision)

    @staticmethod
    def _check_valid_action_parameters(action, frac):
         if (action and frac) or (action is None and frac is None): 
             raise ValueError('You must pass action or frac parameters')








