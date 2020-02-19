from pymongo import MongoClient

class DataBase:
    def __init__(self, name_database):
        self.database = MongoClient()[name_database]
