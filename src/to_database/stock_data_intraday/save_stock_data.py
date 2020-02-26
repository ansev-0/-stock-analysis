from src.to_database.stock_data_intraday import todatabase_intraday
from src.to_database.stock_data_intraday import from_alphavantage
from src.to_database.stock_data_intraday.errors.check_save_stock_data \
    import CheckErrorsSaveStockDataIntraday
from src.acquisition_incidents.incidents import AcquisitionIncidents
from src.database.database import DataBase

class SaveStockData(DataBase):

    def __init__(self, api, apikey, class_save, frecuency, **kwards):
        self.api = api
        self.__check_errors = CheckErrorsSaveStockDataIntraday(api=api)
        #check api supported
        self.__check_errors.check_api_supported()
        #check method of class
        self.__check_errors.check_methods_supported(class_save)
        self.to_database = class_save(frecuency=frecuency, apikey=apikey, **kwards)
        #create connect with collection of orders
        super().__init__(name_database='acquisition_orders')
        #Create object to report incidents saving data
        self.incidents = AcquisitionIncidents()

        
    @classmethod
    def from_alphavantage(cls, frecuency, apikey, **kwards):
        return cls(api='alphavantage',
                   apikey=apikey,
                   frecuency=frecuency,
                   class_save=from_alphavantage.ToDataBaseIntradayAlphaVantageMany,
                   **kwards)
   
    def __get_orders(self, stock_names):

        '''
        This function returns a list with the labels of the names of the companies to read,
        the source can be a docmuento of the database or a list given as an argument.

        Parameters
        --------
        stock_names: list of labels or None

        Return
        ---------
        type: list

        ---> stock_names if stock_names is a valid list.

        ---> list of acquisition_orders database and collection sotck_data_intraday
             if stock_names is None. The list is selected depending on api to get data.
        '''
        
        if  stock_names is None:
            return self.database['stock_data_intraday'].find_one({'_id' : self.api},
                                                                 projection='orders')['orders']
        self.__check_errors.check_list_stocks_name(stock_names)
        return  stock_names
        

    def save_reporting_errors(self, attemps, stock_name=None):
        
        '''
        This function save in database the orders and report errors after n attemps.
        '''
        
        data=self.__get_orders(stock_name)
        errors=self.to_database.to_database_getting_errors(data) 
        if errors:
            return self.__check_and_report_errors(attemps=attemps, errors=errors)
        return None

    def save_ignoring_errors(self, stock_name=None):
        data=self.__get_orders(stock_name)
        self.to_database.to_database_ignoring_errors(data)


    def __report_many_incidents(self, dict_tuple_errors):
        return map(self.__report_incident, [*dict_tuple_errors.values()])



    def __report_incident(self, tuple_error):
        return self.incidents.report(api=self.api,
                                     **dict(zip(self.incidents.report.__code__.co_varnames[-2:],
                                            tuple_error)
                                            )
                                    )

    def __check_and_report_errors(self, attemps, errors):
        new_errors=errors
        count_attemps=1
        while count_attemps < attemps:
            count_attemps+=1
            new_errors=self.to_database.to_database_reporting_errors(list(new_errors)) 
            if not new_errors: 
                return None
        self.__report_many_incidents(new_errors)
        return new_errors




        

        
    