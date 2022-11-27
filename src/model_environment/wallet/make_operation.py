class MakeOperation:

    def __init__(self, validate_operation, modify_wallet):
        self.validate_operation = validate_operation
        self.modify_wallet = modify_wallet

    def __call__(self, wallet, operation):
        wallet_work = wallet.copy()

        if self.validate_operation.sales(wallet_work, operation):
            self.modify_wallet.sales(wallet_work, operation.sales)
        else:
            return False, wallet    
        if self.validate_operation.purchases(wallet_work, operation):
            self.modify_wallet.purchases(wallet_work, operation.purchases)
            wallet = wallet_work
            return True, wallet
        return False, wallet

