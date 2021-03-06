from src.data_preparation.database.database import DataPreparationDataBase

#from pymongo import MongoClient
#from src.database.database import DataBase
#DataBase.set_client(MongoClient())

class PipelineDataBase(DataPreparationDataBase):
    _collection = 'pipeline'

    def __init__(self):
        super().__init__()
        self._collection_connection = self._database.database[self.collection_name]

class Priority(PipelineDataBase):

    _document = 'priority'
    @property
    def document_name(self):
        return self._document

    def get(self, class_name):
        response = self._collection_connection.find_one({'_id' : self._document},
                                                        projection={class_name: True})
        if response: 
            return response[class_name]
        return None 

