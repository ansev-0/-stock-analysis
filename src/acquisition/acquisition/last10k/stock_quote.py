from src.acquisition.acquisition.last10k.last10k import Last10K

class StockQuote(Last10K):
    @Last10K._get_data
    def get(self):
        return 'quote'