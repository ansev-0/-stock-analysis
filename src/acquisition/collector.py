from src.acquisition.to_database.stock_data.save_from_api import SaveStockDataFromApi
from src.tools.inputs import Input
from pymongo import MongoClient
from src.database.database import DataBase


class Menu:

    def __init__(self, options_menu, switch_functions):
        self.options_menu = options_menu
        self.switch_functions = switch_functions

    def ask_for_selection(self, message):
        print(self.options_menu)
        return input(message)


    def run(self):
        selection = self.ask_for_selection(message='Enter One: ')
        while selection != 'quit':
            try:
                self.switch_functions[selection]()
            except Exception:
                selection = self.ask_for_selection(message='Please enter a valid one: ')
            else:
                selection = self.ask_for_selection(message='Enter One: ')

class AcquisitionOrdersMenu(Menu):

    options_menu={'1' : 'Get acquisition orders',
                  '2' : 'Delete all acquisition orders',
                  '3' : 'Update acquisition orders',
                  'quit' : 'no more actions'}

    def __init__(self, controller):
        self.controller=controller
        self.switch_functions={'1' : self.get_acquistion_orders,
                               '2' : self.delete_acquisition_orders,
                               '3' : self.set_acquisition_orders}

        super().__init__(options_menu=self.options_menu, switch_functions=self.switch_functions)

    def get_acquistion_orders(self):
        try:
            acquisition_orders=self.controller.get_acquistion_orders_from_database()
            print('Acquistion orders: \n:',acquisition_orders)
            return acquisition_orders
        except Exception as error:
            print('error getting acquisition orders!')
            return error

    def delete_acquisition_orders(self):
        try:
            delete=self.controller.delete_acquisition_orders()
            print('Orders removed successfully')
            return delete
        except Exception as error:
            print('error deleting acquisition orders!')
            return error

    def set_acquisition_orders(self):
        try:
            orders=self.controller.set_acquisition_orders()
            print('orders successfully established')
            return orders
        except Exception as error:
            print('error setting orders!')
            return error

    

class SaveStockDataMenu(Menu):

    options_menu={'1' : 'save and show errors errors',
                  '2' : 'save ignoring errors',
                  'quit' : 'no more actions'}

    def __init__(self, controller):
        self.switch_functions={'1' : self.save_reporting_errors,
                               '2' : self.save_ignoring_errors,
                               }
        super().__init__(options_menu=self.options_menu, switch_functions=self.switch_functions)
        self.controller=controller

    def save_reporting_errors(self):

        attemps=int(input('Please enter attemps: '))
        if not isinstance(attemps, int):
            raise ValueError('You must enter a integer')
        try:
            errors=self.controller.save_reporting_errors(attemps=attemps, stock_name=self.__get_stock_names())
            print('Errors: \n:', '_'*50, errors)
            return errors
        except Exception as error:
            print('\nFail save reporting errors: ', error)
            return error
        
    
    def save_ignoring_errors(self):
        try:
            save=self.controller.save_ignoring_errors(stock_name=self.__get_stock_names())
            print('Save ignoring errors succesfully')
            return save
        except Exception as error:
            print('\nFail save ingnoring errors: ', error)
            return error

    @staticmethod
    def __get_stock_names():
        stock_name=None
        orders=input('Do you want enter a list of orders?: (yes or no) ')
        if orders=='yes':
            stock_name = Input().get_list()
        return stock_name

    
class IncidentsMenu(Menu):

    options_menu={'1' : 'Get all incidents',
                  '2' : 'Get incident',
                  '3' : 'Delete all incident',
                  '4' : 'Delete incident',
                  'quit' : 'no more actions'}

    def __init__(self, controller):
        self.switch_functions={'1' : self.get_all_incidents,
                               '2' : self.get_incident,
                               '3' : self.delete_all_incidents,
                               '4' : self.delete_incident}
        super().__init__(options_menu=self.options_menu, switch_functions=self.switch_functions)
        self.controller=controller
    
    def get_all_incidents(self):
        try:
            incidents=self.controller.get_all_incidents()
            print('\nIncidents received successfully', '\n', '-'*50)
            for incident in incidents:
                print(incident,'\n', '_'*50, '\n')
            return incidents
        except Exception as error:
            print('Fail getting incidents', error)
            return error

    def get_incident(self):
        try:
            query=int(input('Please enter query: '))
            incident=self.controller.get_incident(query=query)
            print('\nIncident received successfully ','_'*50, incident)
            return incident
        except Exception as error:
            print('Fail getting incident', error)
            return error

    def delete_all_incidents(self):
        try:
            delete=self.controller.delete_all_incidents()
            print('Incidents removed successfully: \n', delete)
            return delete
        except Exception as error:
            print('Fail removing incidents', error)
            return error

    def delete_incident(self):
        try:
            query=int(input('Please enter query: '))
            delete=self.controller.delete_incident(query=query)
            print('Incident removed successfully: \n', delete)
            return delete
        except Exception as error:
            print('Fail removing incident', error)
            return error
        
    



class MainMenu(Menu):

    options_menu={'1' : 'acquisition orders',
                  '2' : 'save stock data',
                  '3' : 'incidents',
                  'quit' : 'no more actions'}

    def __init__(self):
        
        self.__class_controller=self.__get_class_controller()
        self.controller_config()
        self.acquisition_orders_menu = AcquisitionOrdersMenu(controller=self.controller)
        self.save_stock_data_menu = SaveStockDataMenu(controller=self.controller)
        self.incidents_menu = IncidentsMenu(controller=self.controller)

        self.switch_functions={'1' : self.acquisition_orders_menu.run,
                               '2' : self.save_stock_data_menu.run,
                               '3' : self.incidents_menu.run}

        super().__init__(options_menu=self.options_menu, switch_functions=self.switch_functions)

    def controller_config(self):
        controller_config = dict(**self.__get_class_parameters(), **self.__get_others_params())
        self.controller = self.__class_controller(**dict({'api' : self.__api}, **controller_config))

    def __get_others_params(self):
        print('You can enter a dict of others params. \n')
        try:
            return Input().get_dict()
        except Exception:
            return {}

    def __get_class_parameters(self):
        apikey=input('Please enter apikey:\n')
        others_class_params={}
        if 'intraday' in self.__class_controller.__name__:
            others_class_params['frecuency'] = input('Please enter frecuency:\n')
        
        return dict({'apikey' : apikey}, **others_class_params)

    def __get_class_controller(self):
        mapper = {'intraday' : {'alphavantage' : SaveStockDataFromApi.intraday_alphavantage},
                  'daily_adjusted' : {'alphavantage' : SaveStockDataFromApi.dailyadj_alphavantage}}
        
        stock_data_type = input('Please enter stock data type:\n')
        try:

            api_mapper = mapper[stock_data_type]
        except Exception:
            raise ValueError('Invalid stock data type')
        else:
            api=input('Please enter api:\n')
            try:
                class_save=api_mapper[api]
            except Exception:
                raise ValueError('Invalid api')
            else:
                self.__api = api
                self.__stock_data_type = stock_data_type
                return class_save

    
DataBase.set_client(client=MongoClient())
MainMenu().run()
#O39L8VIVYYJYUN3P
