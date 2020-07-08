from src.database.database import DataBase

class TrainAdmin:
    
    __SUPPORTED_DATABASE = ['train_orders', 'train_results']
    
    def __init__(self, database_name, collection, document_id):
        self.check_supported(database_name)
        self.__database = DataBase()
        self.__database.connect(database_name)
        self._collection = self.__database.database[collection]
        self._document_id = document_id
        
        
    def check_supported(self, name):
        if name not in self.__SUPPORTED_DATABASE:
            raise ValueError(f'the databases supported by this class are:\
                             {self.__SUPPORTED_DATABASE}')
            
            
class TrainAdminOrder(TrainAdmin):
    
    def __init__(self, collection, document_id):
        super().__init__(self, 'train_orders', collection, document_id)
        
    def get(self, **kwargs):
        return self._collection.find_one({'_id' : self._document_id}, **kwargs)
            
    def push(self, order, **kwargs):
        return self._collection.update_one({'_id' : self._document_id},
                                           {'$set' : order},
                                           upsert=True,
                                           **kwargs)
        
    def delete(self, **kwargs):
        return self._collection.delete_one({'_id' : self._document_id}, **kwargs)
            

class TrainAdminResults(TrainAdminOrder):
    
    def __init__(self, collection, document_id):
        super().__init__(self, 'train_results', collection, document_id)
        
    def get(self, **kwargs):
        return self._collection.find_one({'_id' : self._document_id}, **kwargs)
            
    def push(self, result, **kwargs):
        return self._collection.update_one({'_id' : self._document_id},
                                           {'$set' : result},
                                           upsert=True,
                                           **kwargs)
    def delete(self, **kwargs):
        return self._collection.delete_one({'_id' : self._document_id}, **kwargs)
    