from src.database.database import DataBaseAdminTiingo
from pymongo import DESCENDING
class LastUpdateNews(DataBaseAdminTiingo):


    def __init__(self, ticker):
        super().__init__(database_name='tiingo_news')
        self._collection = self._database[ticker]

    @property
    def collection(self):
        return self._collection
        
    @property
    def ticker(self):
        return self._collection

    @DataBaseAdminTiingo.try_and_wakeup
    def __call__(self):
        return list(self._collection.find({}, projection={'_id' : True}).sort('_id', DESCENDING).limit(1))[-1]['_id']

