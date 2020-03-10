from src.to_database.stock_data.intraday.save_from_api import SaveIntradayFromApi

class ControllerSaveIntradayFromApi(SaveIntradayFromApi):

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