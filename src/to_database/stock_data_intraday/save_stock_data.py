from src.to_database.stock_data_intraday import from_alphavantage
from src.to_database.stock_data_intraday.errors.check_save_stock_data \
    import CheckErrorsSaveStockDataIntraday
from src.acquisition_incidents.incidents import AcquisitionIncidents
from src.acquisition_orders.acquisition_orders import AcquisitionOrders


class SaveStockData:

    def __init__(self, api, apikey, class_save, frecuency, **kwards):
        self.api = api
        self.check_errors = CheckErrorsSaveStockDataIntraday(api=api)
        #check api supported
        self.check_errors.check_api_supported()
        #check method of class
        self.check_errors.check_methods_supported(class_save)
        self.to_database = class_save(frecuency=frecuency, apikey=apikey, **kwards)
        #create connect with orders
        self.acquistion_orders = AcquisitionOrders(collection='stock_data_intraday')
        #Create object to report incidents saving data
        self.aquisition_incidents = AcquisitionIncidents()

    def get_acquistion_orders_from_database(self):
        return self.acquistion_orders.get_acquisition_api_orders(api=self.api)

    def save_reporting_errors(self, attemps, stock_name=None):
        '''
        This function save in database the orders and report errors after n attemps.
        '''

        errors = self.to_database.to_database_getting_errors(self.__get_orders(stock_name))
        if errors:
            return self.__check_and_report_errors(attemps=attemps, errors=errors)
        return None

    def save_ignoring_errors(self, stock_name=None):
        '''
        This function save in database and return None always.
        '''
        self.to_database.to_database_ignoring_errors(self.__get_orders(stock_name))


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
            return self.get_acquistion_orders_from_database()
        self.check_errors.check_list_stocks_name(stock_names)
        return  stock_names

    def __report_many_incidents(self, dict_tuple_errors):
        return [self.__report_incident(tuple_errors) for tuple_errors in dict_tuple_errors.values()]


    def __report_incident(self, tuple_error):
        print(tuple_error)
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
            count_attemps += 1
            new_errors = self.to_database.to_database_reporting_errors(list(new_errors))
            if not new_errors:
                return None
        self.__report_many_incidents(new_errors)
        return new_errors




class ControllerSaveStockData(SaveStockData):

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
    