from src.to_database.check_errors import CheckToDataBase

class CheckToDataBaseIntraday(CheckToDataBase):

    __NAME_COLLECTION_CHECK_INTRADAY = 'intraday'
    __ID_DOCUMENT = None

    def __init__(self, name):
        #Connect with DataBase
        super().__init__(self, name=name, collection=self.__NAME_COLLECTION_CHECK_INTRADAY) 
        
    def  __get_supported_parameters(self, document_id):
        return self.collection.find_one(filter={'_id' : document_id})

    def update_supported_parameters(self):

        if self.__ID_DOCUMENT is not None:
            self.parameters = (
                self.__get_supported_parameters(document_id=self.__ID_DOCUMENT)
                )

    def set_parameters_database(self, document_id, dict_parameters):
        self.collection.update_one(filter={'_id' : document_id},
                                    update={'$set' : dict_parameters},
                                    upsert=True)

    def delete_parameters_database(self, document_id):
        self.collection.deleten_one(filter={'_id' : document_id})

    






    






