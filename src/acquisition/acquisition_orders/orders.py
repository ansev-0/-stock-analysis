from src.database.database import DataBaseAdminAcquisition

class AcquisitionOrders(DataBaseAdminAcquisition):

    def __init__(self, collection):

        super().__init__('acquisition_orders')
        self.collection=self.database[collection]

    @DataBaseAdminAcquisition.try_and_wakeup
    def set_acquisition_api_orders(self, api, list_orders, **kwargs):
        return self.collection.update_one(filter={'_id' : api},
                                   update={'$set' : {'orders': list_orders}},
                                   upsert=True, 
                                   **kwargs)

    @DataBaseAdminAcquisition.try_and_wakeup
    def delete_acquisition_api_orders(self, api):
        return self.collection.delete_one(query={'_id' : api})

    @DataBaseAdminAcquisition.try_and_wakeup
    def delete_acquisition_orders(self):
        return self.collection.delete_many(query={})

    @DataBaseAdminAcquisition.try_and_wakeup
    def get_acquisition_api_orders(self, api):
        return self.collection.find_one(filter={'_id' : api},
                                        projection={'orders' : 1})['orders']
                                        
    @DataBaseAdminAcquisition.try_and_wakeup
    def get_acquisition_orders(self):
        return  [order['orders'] 
                 for order in self.collection.find(filter={},
                                                   projection={'orders' : 1})]
