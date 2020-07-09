from pymongo import MongoClient

class DataBase:
    '''
    This class creates the connection with the dababase specified.
    '''
    
    def __init_subclass__(cls):
        cls._client = MongoClient('192.168.1.37', 27017)
        
    def __init__(self, database_name):
        try:
            self._database = self._client[database_name]
        except Exception as error:
            print(f'It was not possible to create database connection {database_name}\n', error)
            
    @property
    def database(self):
        return self._database


class DataBaseAdminAcquisition(DataBase):
    '''
    This class is used to create the client
    to connect to the databases related to the acquisition of external data.
    '''
    pass


class DataBaseAdminDataReader(DataBase):
    '''
    This class is used to create the client to read data.
    '''
    pass

class DataBaseAdminDataDataPreparation(DataBase):
    '''
    This class is used to create the client related to the data preparation process.
    '''
    pass

class DataBaseAdminTrain(DataBase):
    '''
    This class is used to create the client related to the data preparation process.
    '''
    pass

