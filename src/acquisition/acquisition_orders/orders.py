from src.database.database import DataBaseAdminAcquisition

class AcquisitionOrders(DataBaseAdminAcquisition):

    def __init__(self, collection):

        super().__init__('acquisition_orders')
        self.collection=self.database[collection]

    def set_acquisition_api_orders(self, api, list_orders, **kwargs):
        return self.collection.update_one(filter={'_id' : api},
                                   update={'$set' : {'orders': list_orders}},
                                   upsert=True, 
                                   **kwargs)

    def delete_acquisition_api_orders(self, api):
        return self.collection.delete_one(query={'_id' : api})

    def delete_acquisition_orders(self):
        return self.collection.delete_many(query={})

    def get_acquisition_api_orders(self, api):
        return self.collection.find_one(filter={'_id' : api},
                                        projection={'orders' : 1})['orders']
    
    def get_acquisition_orders(self):
        return  [order['orders'] 
                 for order in self.collection.find(filter={},
                                                   projection={'orders' : 1})]
