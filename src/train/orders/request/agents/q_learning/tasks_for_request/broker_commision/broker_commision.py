from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    forex_data.forex_data import ForexDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    need_exchange import NeedExchangeTask

class BrokerCommisionTask:

    _forex_data_task = ForexDataTask()

    def _init__(self, broker):
        self.broker = broker

    def __call__(self, index_train, index_val, delays):

        return tuple(self._forex_data_task(from_symbol, to_symbol, 
                                           index_train, index_val, 
                                           delays) 
                     for from_symbol, to_symbol in self._need_broker_exchange)

    @property
    def broker(self):
        return self._broker
    
    @broker.setter
    def broker(self, broker):
        self._need_broker_exchange = NeedExchangeTask(broker)()
        self._broker = broker