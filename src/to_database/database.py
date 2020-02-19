from pymongo import MongoClient
class DataBase:
    def __init__(self,name_database):
        self.db = MongoClient()[name_database]