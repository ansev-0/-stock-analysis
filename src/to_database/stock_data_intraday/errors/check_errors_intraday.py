from src.to_database.check_errors import CheckToDataBase

class CheckToDataBaseIntraday(CheckToDataBase):

    __NAME_COLLECTION_CHECK_INTRADAY = 'intraday'

    def __init__(self):
        super().__init__() #Connect with DataBase
        self.__collection = self.database[self.__NAME_COLLECTION_CHECK_INTRADAY]

    @staticmethod
    def __frecuency_supported(frecuency, list_frecuencies):
        if frecuency in list_frecuencies:
            return True
        return False

    
    def __get_supported_frequencies(self, document_id):
        return self.__collection.find_one(filter = {'_id' : document_id},
                                          projection = {'frecuencies' : True})





    






