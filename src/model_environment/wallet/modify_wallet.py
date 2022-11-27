from src.model_environment.wallet.operation import Operation
from src.model_environment.wallet.wallet import Wallet
from src.model_environment.wallet.calculate_money_transactions  import calculate_money_operations
import numpy as np

class ModifyWallet:

    def sales(self, wallet, sales):
        for name_stock, (amount, _) in sales.items():
            wallet.remove_stock(name_stock, amount)
        wallet.money += calculate_money_operations(sales)
        return wallet

    def purchases(self, wallet, purchases):
        for name_stock, (amount, price) in purchases.items():
            wallet.add_stock(name_stock, amount)
        wallet.money -= calculate_money_operations(purchases)
        return wallet

