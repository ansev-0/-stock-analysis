from src.exceptions.to_database_exceptions import ToDataBaseError
from pymongo import MongoClient

class CheckErrorsToDataBase:

    list_databases = MongoClient().list_database_names()

    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: if_not_in_base', ValueError)

    def check_database_exists(self, database_name):
        if not database_name in self.list_databases:
            raise ToDataBaseError('DataBase not supported', ValueError)


    
