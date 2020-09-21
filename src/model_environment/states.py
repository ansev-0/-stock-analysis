
class States:


    def __init__(self, time_serie, init_n_stocks, init_money, commision):

        self.time_serie = time_serie
        self.n_stocks = None
        self.money = None
        self.time = None
        self.terminal = False
        self.init_n_stocks = init_n_stocks
        self.init_money = init_money
        self.commision = commision
        

        self.reset()

    @property
    def init_stock_price(self):
        return self.time_serie[0]

    @property
    def stock_price(self):
        return self.time_serie[self.time]

    @property
    def init_inventory_price(self):
        return self.init_n_stocks * (self.init_stock_price - self.commision)

    @property
    def inventory_price(self):
        return self.n_stocks * (self.stock_price - self.commision)

    @property
    def init_gross_inventory_price(self):
        return self.init_n_stocks * self.init_stock_price

    @property
    def gross_inventory_price(self):
        return self.n_stocks * self.stock_price

    @property
    def profit(self):
        return self.inventory_price + self.money - self.init_money - self.init_inventory_price

    @property     
    def inventory_empty(self):
        return self.n_stocks > 0

    def step(self):
        self.time += 1
        self._stock_price = self.time_serie[self.time]
        self.terminal = self.time == len(self.time_serie) - 1
        
    def reset_n_stocks(self):
        self.n_stocks = self.init_n_stocks

    def reset_money(self):
        self.money = self.init_money

    def reset_time(self):
        self.time = 0

    def reset(self):
        self.terminal = False
        self.reset_money()
        self.reset_n_stocks()
        self.reset_time()
    


    