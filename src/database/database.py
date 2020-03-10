from pymongo import MongoClient

class DataBase:
    '''
    This class creates the connection with the dababase specified
    '''
    def __init__(self, database_name):
        self.database = MongoClient()[database_name]
