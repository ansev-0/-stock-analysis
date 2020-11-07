from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    forex_data.forex_data import ForexDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.broker_commision.\
    need_exchange import NeedExchangeTask

class BrokerCommisionTask:

    _forex_data_task = ForexDataTask()

    def __init__(self, broker):
        self.broker = broker

    def __call__(self, index_train, index_val, delays):

        return tuple(self._get_commision_for_index(index, delays) 
                     for index in (index_train, index_val))




    def _get_commision_for_index(self, index, delays):

        return {commision_type : {'cache_id' : self._forex_data_task(*data['symbols'], index, delays),
                                  'value' : data['value']} \
                if isinstance(data, dict) else {'value' : data} \
                for commision_type, data in self._need_broker_exchange.items()}


    @property
    def broker(self):
        return self._broker
    
    @broker.setter
    def broker(self, broker):
        self._need_broker_exchange = NeedExchangeTask(broker)()
        self._broker = broker