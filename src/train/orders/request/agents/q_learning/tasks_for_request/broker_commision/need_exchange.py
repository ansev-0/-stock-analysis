from src.brokers.database.find import FindBrokers

class NeedExchangeTask:

    def __init__(self, broker):
        self.broker = broker

    @property
    def broker(self):
        return self._broker
    
    @broker.setter
    def broker(self, broker):
        self._find_broker = FindBrokers(broker)
        self._broker = broker


    def __call__(self):

        return tuple(
            ('USD', unit) for unit in
            map(
                lambda commision: commision['units'],
                self._broker.find_one({'_id' : 'commision'},
                                      projection={'_id' : 0}).values()
                )
            if unit != 'USD'

        )
        