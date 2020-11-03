from src.database.database import DataBaseAdminAcquisition
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveFromApi(DataBaseAdminAcquisition):

    def __init__(self, api, collection):
        #self.__database = DataBase()
        #self.connect(database_name='api_features')
        super().__init__('api_features')
        self.api = api
        self.collection = collection

    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in list_apis:
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)
    def __get_apis(self):
        return list(map(lambda x: x['_id'], self.database[self.collection].find({}, projection='_id')))
