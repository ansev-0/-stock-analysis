from src.exceptions.to_database_exceptions import ToDataBaseError
from pymongo import MongoClient

class CheckErrorsUpdateDataBase:


    @staticmethod
    def check_parameter_create(create):
        if create  not in ['create', 'not create']:
            raise ToDataBaseError('Invalid parameter: new_database', ValueError)

    def check_database_exists(self, database_name):
        list_database = MongoClient('192.168.1.37', 27017).list_database_names()
        if not database_name in list_database:
            raise ToDataBaseError('DataBase not supported', ValueError)


    
