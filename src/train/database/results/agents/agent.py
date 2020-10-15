from src.database.database import DataBaseAdminTrain

class ResultTrainDataBase(DataBaseAdminTrain):

    def __init__(self, stock_name):
        super().__init__('results_train')
        self.collection = stock_name
    
    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, stock_name):
        self._collection = self._database[stock_name]

