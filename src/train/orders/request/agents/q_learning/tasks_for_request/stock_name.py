from src.read_database.stock_data import StockDataFromDataBase

class StockNameTask:
    _reader = reader = StockDataFromDataBase.dailyadj_dataframe()

    def __call__(self, stock_name):
        self._check_stock_name_in_db(stock_name)
        return stock_name

    def _check_stock_name_in_db(self, stock_name):
        if not stock_name in self.reader.database.list_collection_names():
            raise ValueError('You must pass a valid stock name')
