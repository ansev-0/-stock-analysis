from src.acquisition.acquisition_incidents.incidents import AcquisitionIncidents
from src.acquisition.acquisition_orders.orders import AcquisitionOrders
from src.view.acquisition.to_database.stock_data.show_status.status_save_stock_data import SaveStockDataShowStatus
from src.acquisition.to_database.stock_data.errors.check_save_from_api \
    import CheckErrorsSaveStockDataFromApi
from src.acquisition.to_database.stock_data.intraday import from_alphavantage as intraday_alphavantage
from src.acquisition.to_database.stock_data.daily_adjusted import from_alphavantage as dailyadj_alphavantage


class SaveStockDataFromApi:

    def __init__(self, api, collection, data_collector):
        self.api = api
        self.check_errors = CheckErrorsSaveStockDataFromApi(api=api, collection=collection)
        #check api supported
        self.check_errors.check_api_supported()
        #Get object to save 
        self.to_database = data_collector
        #Check object has methods to save
        self.check_errors.check_methods_supported(self.to_database)
        #create connect with orders
        self.acquistion_orders = AcquisitionOrders(collection=collection)
        #Create object to report incidents saving data
        self.aquisition_incidents = AcquisitionIncidents()
        #Create object to show show_status process
        self.show_status=SaveStockDataShowStatus()


    def save_reporting_errors(self, attemps, stock_name=None):
        '''
        This function save in database the orders and report errors after n attemps.
        '''
        self.show_status.notify_init_save_process()
        errors = self.to_database.to_database_getting_errors(self.__get_orders(stock_name))
        if errors:
            self.show_status.notify_there_have_been_errors(companies=list(errors))
            return self.__check_and_report_errors(attemps=attemps, errors=errors)
        return None

    def save_ignoring_errors(self, stock_name=None):
        '''
        This function save in database and return None always.
        '''
        self.to_database.to_database_ignoring_errors(self.__get_orders(stock_name))



    def get_acquistion_orders_from_database(self):
        return self.acquistion_orders.get_acquisition_api_orders(api=self.api)


    def set_acquisition_orders(self, list_orders):
        self.check_errors.check_list_stocks_name(list_orders)
        return self.acquistion_orders.set_acquisition_api_orders(api=self.api,
                                                                 list_orders=list_orders)
    def delete_acquistion_orders(self):
        return self.acquistion_orders.delete_acquisition_api_orders(api=self.api)

    def get_all_incidents(self):
        return self.aquisition_incidents.get_all_incidents(api=self.api)

    def get_incident(self, query):
        return self.aquisition_incidents.get_incident(api=self.api, query=query)
    
    def delete_all_incidents(self):
        return self.aquisition_incidents.delete_all_incidents(api=self.api)

    def delete_incident(self, query):
        return self.aquisition_incidents.delete_incident(api=self.api, query=query)

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
            return self.get_acquistion_orders_from_database()
        self.check_errors.check_list_stocks_name(stock_names)
        return  stock_names

    def __report_many_incidents(self, dict_tuple_errors):
        return [self.__report_incident(tuple_errors) for tuple_errors in dict_tuple_errors.values()]


    def __report_incident(self, tuple_error):
        return self.aquisition_incidents.report(api=self.api,
                                                **dict(
                                                    zip(self.aquisition_incidents
                                                        .report.__code__.co_varnames[-2:],
                                                        tuple_error))
                                                )

    def __check_and_report_errors(self, attemps, errors):
        new_errors = errors
        count_attemps = 1
        while count_attemps < attemps:
            self.show_status.notify_try_again(count_attemps)
            count_attemps += 1
            new_errors = self.to_database.to_database_getting_errors(list(new_errors))
            if not new_errors:
                return None
        self.__report_many_incidents(new_errors)
        return new_errors

    @classmethod
    def intraday_alphavantage(cls, frecuency, apikey, **kwargs):
        class_collector = cls.__get_intraday_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(frecuency=frecuency,
                                                  apikey=apikey, **kwargs),
                   collection='stock_data_intraday')
    @classmethod
    def dailyadj_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_dailyadj_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='stock_data_dailyadj')

    @classmethod
    def __get_intraday_collector(cls, api):
        return {'alphavantage' : intraday_alphavantage.UpdateIntradayAlphaVantageMany}[api]

    @classmethod
    def __get_dailyadj_collector(cls, api):
        return {'alphavantage' : dailyadj_alphavantage.UpdateDailyAdjAlphaVantageMany}[api]

