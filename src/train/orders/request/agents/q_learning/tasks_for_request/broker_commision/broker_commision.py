from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    forex_data.forex_data import ForexDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    need_exchange import NeedExchangeTask

class BrokerCommisionTask:

    _forex_data_task = ForexDataTask()

    def __init__(self, broker):
        self.broker = broker

    def __call__(self, index_train, index_val, delays):

        commision_dict = {commision_type : self._forex_data_task(*symbols, 
                                           index_train, index_val, 
                                           delays) 
                          for commision_type, symbols in self._need_broker_exchange.items()}

        return self._get_dict_output(commision_dict)

    @staticmethod
    def _get_dict_output(commmision_dict):
        tup = {}, {}
        for key, value in commmision_dict.items():
            for i, val in enumerate(value):
                tup[i][key] = val
        return tup

    @property
    def broker(self):
        return self._broker
    
    @broker.setter
    def broker(self, broker):
        self._need_broker_exchange = NeedExchangeTask(broker)()
        self._broker = broker