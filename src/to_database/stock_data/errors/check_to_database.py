from src.exceptions.to_database_exceptions import ToDataBaseError
from src.database.database import DataBase

class CheckErrorsToDataBase:

    __database = DataBase()
    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_database_exists(self, database_name):
        list_database = self.__database.client.list_database_names()
        if not database_name in list_database:
            raise ToDataBaseError('DataBase not supported', ValueError)


    
