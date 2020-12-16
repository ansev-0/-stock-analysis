from abc import ABCMeta, abstractproperty
from src.acquisition.acquisition_incidents.incidents import AcquisitionIncidents
from src.acquisition.acquisition_orders.orders import AcquisitionOrders

class SaveDataFromApi(metaclass=ABCMeta):

    def __init__(self, api, collections, data_collector):
        self.api = api
        #check api supported
        self.check_errors.check_api_supported()
        #Get object to save 
        self.to_database = data_collector
        #Check object has methods to save
        self.check_errors.check_methods_supported(self.to_database)
        #create connect with orders
        self.acquistion_orders = AcquisitionOrders(collection=self._collection_name(collections))
        #Create object to report incidents saving data
        self.aquisition_incidents = AcquisitionIncidents()

    @abstractproperty
    def check_errors(self):
        pass

    @abstractproperty
    def show_status(self):
        pass

    def save_reporting_errors(self, attemps, list_queries=None):
        '''
        This function save in database the orders and report errors after n attemps.
        '''
        self.show_status.notify_init_save_process()
        errors = self.to_database.to_database_getting_errors(self.__get_orders(list_queries))
        if errors:
            self.show_status.notify_there_have_been_errors(companies=list(errors))
            return self.__check_and_report_errors(attemps=attemps, errors=errors)
        return None

    def save_ignoring_errors(self, list_queries=None):
        '''
        This function save in database and return None always.
        '''
        self.to_database.to_database_ignoring_errors(self.__get_orders(list_queries))


    def get_acquistion_orders_from_database(self):
        return self.acquistion_orders.get_acquisition_api_orders(api=self.api)

    def set_acquisition_orders(self, list_orders):
        self.check_errors.check_list_queries(list_orders)
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

    def __get_orders(self, list_queries):

        '''
        This function returns a list with the labels of the names of the companies to read,
        the source can be a docmuento of the database or a list given as an argument.
        Parameters
        --------
        list_queries: list of labels or None
        Return
        ---------
        type: list
        ---> list_queries if list_queries is a valid list.
        ---> list of acquisition_orders database and collection sotck_data_intraday
                if list_queries is None. The list is selected depending on api to get data.
        '''
        if  list_queries is None:
            return self.get_acquistion_orders_from_database()
        self.check_errors.check_list_queries(list_queries)
        return  list_queries

    def __report_many_incidents(self, dict_tuple_errors):
        return [self.__report_incident(tuple_errors) for tuple_errors in dict_tuple_errors.values()]


    def __report_incident(self, tuple_error):
        return self.aquisition_incidents.report(api=self.api,
                                                **dict(
                                                    zip(self.aquisition_incidents
                                                        .report.__code__.co_varnames[-2:],
                                                        tuple_error))
                                                )

    def _collection_name(self, collections):
        return f'extended_{collections}' if 'extended' in self.to_database.__class__.__name__.lower() \
            else collections

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
