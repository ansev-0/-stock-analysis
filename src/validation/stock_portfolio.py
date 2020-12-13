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
    
    def total_money_in_action(self, stock, current_value):
        return self._shares_of_stock[stock] *current_value
    
    @property
    def shares_of_stock(self):
        return self._shares_of_stock
    
    
    def buy(self, stock, money, verbose=True):
        

        
        if self.money > money:
            
            self._shares_of_stock[stock] +=1
            self._money -= money
            
            print(f'Bought, price {money}\n')
            if verbose:
                self.__print_n_actions_and_money(stock)
            
        elif verbose:
            print(f'Not possible Bought, There are not enough money')
        
    def sell(self, stock, money, verbose=True):
        
        if self._shares_of_stock[stock] >= 1:
            
            self._shares_of_stock[stock] -= 1
            self._money += money
            print(f'Sold, price {money}\n')
            
            if verbose:
                self.__print_n_actions_and_money(stock)
            
        elif verbose:
            print(f'Not possible sell, There are no {stock} shares in the portfolio')
            

        
    def __print_n_actions_and_money(self, stock):
        n_actions = self._shares_of_stock[stock]
        print(f'Number of {stock} shares is now : {n_actions}\n',
                  f'Current money: {self._money}\n')
        