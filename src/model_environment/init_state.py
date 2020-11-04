class InitState:

    def __init__(self,  
                 init_n_stocks, 
                 init_money, 
                 init_stock_price, 
                 commision):

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
        
        return self.gross_inventory_price - self.commision
