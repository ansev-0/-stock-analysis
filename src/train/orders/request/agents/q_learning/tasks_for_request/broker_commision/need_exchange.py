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

        return {commision_type : 
                ('USD', commision['units']) 
                for commision_type, commision in \

                self._find_broker.find_one({'_id' : 'commision'},
                                           projection={'_id' : 0}).items()
                
                if commision['units'] != 'USD'

        }
        