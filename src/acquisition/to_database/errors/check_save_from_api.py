from src.database.database import DataBaseAdminAcquisition
from src.exceptions.to_database_exceptions import ToDataBaseError

class CheckErrorsSaveFromApi(DataBaseAdminAcquisition):

    REQUIRED_METHODS = ('to_database_getting_errors', 'to_database_ignoring_errors')
    
    def __init__(self, api, collection):
        #self.__database = DataBase()
        #self.connect(database_name='api_features')
        super().__init__('api_features')
        self.api = api
        self.collection = collection

    def check_methods_supported(self, object_save):
        for method in self.REQUIRED_METHODS:
            if not hasattr(object_save, method):
                raise ToDataBaseError(f'Invalid class, the class must have:\
                                      {self.REQUIRED_METHODS} methods',
                                      AttributeError)

    def check_api_supported(self):
        list_apis=self.__get_apis()
        if self.api not in list_apis:
            raise ToDataBaseError(f'Invalid API: {self.api}, the valid API are: {list_apis}',
                                  ValueError)
    def __get_apis(self):
        return list(
                    map(lambda x: x['_id'], 
                        self.database[self.collection].find({}, projection='_id'))
                    )
