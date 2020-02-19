import pandas as pd
from src.to_database.stock_data_intraday.todatabase_intraday import ToDataBaseIntraday
from src.acquisition.alphavantage import timeseries
from src.to_database.stock_data_intraday.errors.check_from_alphavantage \
    import CheckErrorsFromAlphaVantage

class ToDataBaseIntradayAlphaVantage(ToDataBaseIntraday):
    def __init__(self, frecuency, apikey, outputsize='full', new_database='create', **kwards):

        #Get outputsize
        self.outputsize = outputsize

        #Check not error in frecunecy
        self.__check_alphavantage = CheckErrorsFromAlphaVantage()
        self.__check_alphavantage.check_frecuency_in_api(frecuency=frecuency)

        #Create connection to the database
        super().__init__(frecuency=frecuency, new_database=new_database)

        # Create reader from AlphaVantage
        self.__reader = timeseries.TimeSeries(apikey=apikey, **kwards)

    def to_database(self, company):
        '''
        This function save in DataBase the data of the specified company,
        when an API error is obtained, the error returns,
        if no error is obtained, nothing returns (None)
        '''

        #Get response from reader Api Alphavantage
        response = self.__read_from_alphavantage(company=company)

        if isinstance(response, list):
            return response

        #Get data
        # list(response) get keys of response dict,
        # the seconds key contains the data,
        # this is test  in AlphaVantage.__read() by:
        #acquistion.errors_response.ErrorsResponseApiAlphavantage().
        key_data = list(response)[1]
        data = response[key_data]
        #check frecuency in key
        self.__check_alphavantage.check_frecuency_in_key_data(key_data, self.frecuency)
        #Update collection
        #Get correct format
        list_dicts_to_update = self.__create_dicts_with_same_id(data)
        #Call to update
        self.update_company_collection(list_dicts_to_update=list_dicts_to_update, company=company)

        return None

    @staticmethod
    def __create_dicts_with_same_id(data):
        '''
        This function adapts the format of the json received from the Alphavantage API
        to the format necessary to update the database using :

        update_company_collection

        '''

        previous_date = None
        list_dicts = []

        for key, value in data.items():
            date = key[:10]
            value = {k1[3:] : v1 for k1, v1 in value.items()}
            if date != previous_date:
                list_dicts.append({'_id':pd.to_datetime(date), 'data':{key : value}})
                previous_date = date
            else:
                list_dicts[-1]['data'].update({key : value})

        return list_dicts

    def __read_from_alphavantage(self, company):
        '''
        This function gets the API response,
        returns a dictionary if the answer does not contain errors,
        and a list if there are errors.
        '''
        return self.__reader.get_intraday(symbol=company,
                                          interval=self.frecuency,
                                          outputsize=self.outputsize)
