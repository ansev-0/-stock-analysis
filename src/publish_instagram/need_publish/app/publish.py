from datetime import datetime
import pandas as pd

class PublishApp:
    
    def __init__(self, connector):
        self._connector = connector
        
    def publish(self, company, data):
        return self._connector.publish(company, data)

    def last_time(self, company):
        get_result = self._connector.get(company, ascending=False)
        try:
            data = next(iter(get_result))
            return pd.to_datetime(data.index[0]), pd.to_datetime(data.index[1])
        except StopIteration:
            # to advise never(contract)
            return datetime(1970, 1, 1), datetime(1970, 1, 1)
        