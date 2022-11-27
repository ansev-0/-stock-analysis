from src.acquisition.to_database.financial_data.update_financial_feature_database import UpdateFinancialFeatureData
from src.acquisition.acquisition.alphavantage.fundamental_data import FundamentalData
from src.acquisition.to_database.save_many_stock_collection import SaveMany
from pandas import to_datetime
from abc import ABCMeta, abstractmethod


class UpdateFinancialFeatureAlphaVantage(metaclass=ABCMeta):
    '''
    This class is an interface to save the financial features data of  Alphavantage API

    '''

    _TYPES_DB = ('annual', 'quarterly')
    _ADD_TYPE = 'Reports'

    @property
    @classmethod
    @abstractmethod
    def feature(cls):
        pass

    def __init__(self, new_database='create', **kwargs):
        '''    
        Parameters
        ----------
        new_database: str
        valid parameters = 'create' and 'not create'
        '''

        # Create connection to the database
        self._init_databases(new_database)
        # Create reader from AlphaVantage
        self.__reader = FundamentalData(**kwargs)

    def to_database(self, company):
        '''
        This function save in DataBase the data of the specified company,
        when an API error is obtained, the error returns,
        if no error is obtained, nothing returns (None)
        '''
        #Get response from reader Api Alphavantage
        response = self.__read_from_alphavantage(company=company)
        if isinstance(response, tuple):
            return response
        #update db
        self._update_database(company, response)
        return None

    def _update_database(self, company, response):
        for type_db, list_to_db in self._to_valid_format(response).items():
            getattr(self, f'_{type_db}_{self.feature}').update(company=company, 
                                                              list_dicts_to_update=list_to_db)

    def _to_valid_format(self, response):
        return {key[:-len(self._ADD_TYPE)] : self._list_to_valid_format(data) 
                for key, data in response.items() 
                if self._ADD_TYPE in key}

    def _list_to_valid_format(self, list_data):
        # rename 
        return [{(key if key != 'fiscalDateEnding'  else '_id') : \
                 (value if key != 'fiscalDateEnding' else to_datetime(value))

                 for key, value in data.items()} 
                for data in list_data]
    
    def __read_from_alphavantage(self, company):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return getattr(self.__reader, f'get_{self.feature}')(symbol=company)

    def _init_databases(self, new_database):
        for type_db in self._TYPES_DB:
            setattr(self, f'_{type_db}_{self.feature}', 
                    UpdateFinancialFeatureData(new_database=new_database, 
                                               database_name=f'{self.feature}_{type_db}'))
