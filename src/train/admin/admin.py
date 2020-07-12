from pymongo import MongoClient
from src.database.database import  DataBaseAdminTrain
from datetime import datetime

class DataBaseAdminTrainOrders(DataBaseAdminTrain):
    
    def __init__(self, train_type):
        super().__init__('train_orders')
        self._train_type = train_type
        self.collection = self._database[train_type]
        
    @property 
    def train_type(self):
        return self._train_type
    

class DataBaseAdminTrainOrdersGenerator(DataBaseAdminTrainOrders):

    __set_init_status_pending = {'$set' : {'status' : 'pending'}}

    def __init__(self, train_type, active,  **kwargs):
        super().__init__(train_type) 
        self._train_parameters = {}
        self._train_parameters['active'] = active
        self._train_parameters['status'] = 'pending'
        self._id = self.__get_id()
        self._train_parameters['_id'] = self._id
        self._train_parameters.update(kwargs)
        
    @property
    def id_train(self):
        return self._id
    
    @property 
    def train_parameters(self):
        return self._train_parameters
        
    def __get_id(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    def push_order(self):
        return self.collection.insert_one(self.train_parameters)
        
    def set_pending_status_in_id_train(self, id_train):
        return self.collection.update_one({'_id' : id_train}, 
                                          self.__set_init_status_pending)
        
    def set_pending_status(self, filter_train):
        return self.collection.update_many(filter_train,
                                           self.__set_init_status_pending)

    def set_pending_status_in_all_running(self):
        return self.collection.update_many({'status' : 'running'},
                                           self.__set_init_status_pending)

    def set_pending_status_in_all_done(self):
        return self.collection.update_many({'status' : 'done'},
                                           self.__set_init_status_pending)
        
        
class DataBaseAdminTrainOrdersGeneratorTimeSeries(DataBaseAdminTrainOrdersGenerator):
    
    def __init__(self, train_start, train_end, delays, **kwargs):
        super().__init__(**kwargs)
        self.train_parameters['train_start'] = train_start
        self.train_parameters['train_end'] = train_end
        self.train_parameters['delays'] = delays
        
        

class DataBaseAdminTrainOrdersGeneratorTimeSeriesOptimizer(DataBaseAdminTrainOrdersGeneratorTimeSeries):
    
        def __init__(self, optimizer_params, **kwargs):
            super().__init__(**kwargs)
            self.train_parameters['optmizer_params'] = optimizer_params
            
            
class DataBaseAdminTrainOrdersSearcher(DataBaseAdminTrainOrders):
    
    def search_by_id_train(self, id_train, **kwargs):
        return self.__find_one({'_id' : id_train}, **kwargs)
    
    def search_by_status(self, status, **kwargs):
        try:
            return list(self.__find({'status' : status}, **kwargs))
        except TypeError:
            return None

    def search_one_by_status(self, status, **kwargs):
        return self.__find_one({'status' : status})
        
    def search_one(self, *args,**kwargs):
        return self.__find_one(*args, **kwargs)
    
    def search_many(self, *args, **kwargs):
        return self.__find(*args, **kwargs)
        
        
    def __find_one(self, filter_train, **kwargs):
        return self.collection.find_one(filter_train, **kwargs)
    
    def __find(self, filter_train, **kwargs):
        return self.collection.find(filter_train, **kwargs)
    
    
class DataBaseAdminTrainOrdersGet(DataBaseAdminTrainOrdersSearcher):
    
    __set_init_status_running = {'$set' : {'status' : 'running'}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_by_id_train(self, id_train, **kwargs):
        order = self.search_by_id_train(id_train, **kwargs)
        self.set_running_status_in_id_train(id_train)
        return order
    
    def get_by_status(self, status, **kwargs):
        order = self.search_by_status(status, **kwargs)
        if order:
            self.set_running_status_in_status(status)
        return order

    def get_first_by_status(self, status, **kwargs):
        order = self.search_one_by_status(status, **kwargs)
        if order:
            self.set_running_status_in_id_train(order['_id'])

        return order

    def get_first_pending(self):
        order = self.search_one_by_status('pending')
        if order:
            self.set_running_status_in_id_train(order['_id'])
        return order
        
    def set_running_status_in_id_train(self, id_train):
        return self.collection.update_one({'_id' : id_train},
                                          self.__set_init_status_running)
    
    def set_running_status_in_status(self, status):
        return self.__set_running_status_many({'status' : status})
        
    def set_running_status(self, filter_train):
        return self.__set_running_status_many(filter_train)
    
    def __set_running_status_many(self, filter_train):
        return self.collection.update_many(filter_train,
                                           self.__set_init_status_running)

        
class DataBaseAdminTrainOrdersUpdateResults(DataBaseAdminTrainOrders):
    
    def update_result(self, id_train, results):
        return self.__update_one({'_id' : id_train}, {'$set' : results})
        
    def update_result_and_status(self, id_train, results):
        return self.__update_one({'_id' : id_train}, {'$set' : dict(results, **{'status' : 'done'})})
        
    def __update_one(self, *args):
        return self.collection.update_one(*args)
    
    
class DataBaseAdminTrainOrdersInterrupt(DataBaseAdminTrainOrders):
    
    __set_init_status_interrupt = {'$set' : {'status' : 'interrupt'}}

    def set_interrupt_status_in_id_train(self, id_train):
        return self.collection.update_one({'_id' : id_train}, self.__set_init_status_interrupt)

    def set_interrupt_all_in_running(self):
        return self. __update_many({'status' : 'running'}, self.__set_init_status_interrupt)
    
    def set_interrupt_status(self, interrupt_filter):
        return self. __update_many(interrupt_filter, self.__set_init_status_interrupt)

    def __update_many(self, *args, **kwargs):
        return self.collection.update_many(*args, **kwargs)
    
        
        
class DataBaseAdminTrainOrdersDelete(DataBaseAdminTrainOrders):  
    
    def delete_by_id_train(self, id_train):
        return self.collection.delete_one({'_id' : id_train})
        
    def delete_by_status(self, status):
        return self.__delete_many({'status' : status})
        
    def delete_many(self, filter_delete):
        return self.__delete_many(filter_delete)
    
    def delete_one(self, filter_delete):
        return self.collection.delete_one(filter_delete)
        
    def __delete_many(self, filter_delete):
        return self.collection.delete_many(filter_delete)
        