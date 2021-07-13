from pymongo import MongoClient
from src.tools.mongodb import restart_connect_mongodb
from pymongo.errors import ServerSelectionTimeoutError
from functools import wraps

class DataBase:
    '''
    This class creates the connection with the dababase specified.
    '''
    
    def __init_subclass__(cls):
        cls._client = MongoClient(host='127.0.0.1', port=27017)
        
    def __init__(self, database_name):
        try:
            self._database = self._client[database_name]
        except Exception as error:
            print(f'It was not possible to create database connection {database_name}\n', error)

    @classmethod
    def try_and_wakeup(cls, function, attemps=2):

        @wraps(function)
        def _try_except_server_selection_time_error(self, *args, **kwargs):

            for _ in range(attemps):
                try:
                    return function(self, *args, **kwargs)

                except ServerSelectionTimeoutError as error:
                    restart_connect_mongodb()
            raise error

        return _try_except_server_selection_time_error

    @property
    def database(self):
        return self._database


class DataBaseAdminAcquisition(DataBase):
    '''
    This class is used to create the client
    to connect to the databases related to the acquisition of external data.
    '''
    pass

class DataBaseAdminAssets(DataBase):
    '''
    This class is used to create the client
    to connect to the databases related to assets.
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
    This class is used to create the client related to the train process.
    '''
    pass

class DataBaseAdminModels(DataBase):
    '''
    This class is used to create the client related to the models.
    '''
    pass

class DataBaseAdminUsers(DataBase):
    '''
    This class is used to create the client related to the users.
    '''
    pass


class DataBaseAdminBrokers(DataBase):
    '''
    This class is used to create the client related to the brokers.
    '''
    pass

class DataBaseAdminCronTab(DataBase):
    '''
    This class is used to create the client related to the CronTab.
    '''
    pass

class DataBaseAdminTwitterRequests(DataBase):
    '''
    This class is used to create the client
    to connect to the databases related to Twitter API.
    '''
    pass

class DataBaseAdminTiingo(DataBase):
    '''
    This class is used to create the client
    to connect to the databases related to Twitter API.
    '''
    pass

