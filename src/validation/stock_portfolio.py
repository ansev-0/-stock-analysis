from collections import defaultdict

class StockPortfolio:
    
    def __init__(self, init_money, init_shares_of_stock = None):
        self._shares_of_stock = defaultdict(int)
        self._money = init_money
        
        if isinstance(init_shares_of_stock, dict):
            self._shares_of_stock.update(init_shares_of_stock)
        
    @property
    def money(self):
        return self._money
    
    @property
    def shares_of_stock(self):
        return self._shares_of_stock
    
    
    def buy(self, stock, money, verbose=True):
        
        self._shares_of_stock[stock] +=1
        self._money -= money
        print('Bought\n')
        
        if verbose:
            self.__print_n_actions_and_money(stock)
        
    def sell(self, stock, money, verbose=True):
        
        if self._shares_of_stock[stock] >= 1:
            
            self._shares_of_stock[stock] -= 1
            self._money += money
            print('Sold\n')
            
            if verbose:
                self.__print_n_actions_and_money(stock)
            
        elif verbose:
            print(f'Not possible sell, There are no {stock} shares in the portfolio')
            

        
    def __print_n_actions_and_money(self, stock):
        n_actions = self._shares_of_stock[stock]
        print(f'Number of {stock} shares is now : {n_actions}\n',
                  f'Current money: {self._money}\n')
        
        