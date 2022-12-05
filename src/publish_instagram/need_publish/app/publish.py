from datetime import datetime
import pandas as pd

class PublishApp:
    
    def __init__(self, connector):
        self._connector = connector
        
    def publish(self, company, data):
        return self._connector.publish(company, data['data'], data['incr'])

    def last_time(self, company):
        get_result = self._connector.get(company, ascending=False)
        try:
            data = next(iter(get_result))
            if data.empty:
                return datetime(1970, 1, 1), datetime(1970, 1, 1)
            return pd.to_datetime(data.index.min()), pd.to_datetime(data.index.max())
        except StopIteration:
            # to advise never (contract)
            return datetime(1970, 1, 1), datetime(1970, 1, 1)
        