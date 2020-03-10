from pymongo import MongoClient

class DataBase:
    '''
    This class creates the connection with the dababase specified
    It is required to establish the client.
    '''

    @classmethod
    def set_client(cls, client):
        cls.client = client
    
    def connect(self, database_name):
        try:
            self.database = self.client[database_name]
        except Exception as error:
            print(f'It was not possible to create database connection{database_name}\n', error)


