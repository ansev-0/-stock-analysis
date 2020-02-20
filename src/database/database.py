from pymongo import MongoClient

class DataBase:
    '''
    This class creates the connection with the dababase specified
    '''
    def __init__(self, name_database):
        self.database = MongoClient()[name_database]
