from src.model_environment.wallet.wallet import Wallet
from src.model_environment.wallet.operation import Operation
from src.model_environment.wallet.calculate_money_transactions  import calculate_money_operations
import numpy as np

class Validate:
    
    def sales(self, wallet, operation):
        assert isinstance(wallet, Wallet)
        assert isinstance(operation, Operation)
        if not operation.sales:
            return True
        for stock_name, (amount, _) in operation.sales.items():
            if not stock_name in wallet.stocks or amount > wallet.stocks[stock_name]:
                return False
        return True

    def purchases(self, wallet, operation):
        assert isinstance(wallet, Wallet)
        assert isinstance(operation, Operation)
        if not operation.purchases:
            return True
        return calculate_money_operations(operation.purchases) <= wallet.money
 