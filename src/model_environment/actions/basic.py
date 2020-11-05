from abc import ABCMeta, abstractproperty

class BasicActions:

    @abstractproperty
    def commision_costs(self):
        pass

    @abstractproperty
    def n_stocks(self):
        pass

    @abstractproperty
    def money(self):
        pass

    @abstractproperty
    def stock_price(self):
        pass

    def order_sell(self, n_stocks):

        self.n_stocks -= n_stocks
        self.money += n_stocks * self.stock_price - self.commision_costs

    def order_buy(self, n_stocks):
        self.n_stocks += n_stocks
        self.money -= n_stocks * self.stock_price + self.commision_costs