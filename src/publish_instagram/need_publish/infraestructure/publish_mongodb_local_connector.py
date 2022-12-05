from src.database.database import DataBasePublishInstagram
from datetime import datetime
import pandas as pd

class MongoDBLocalConnector(DataBasePublishInstagram):
    
    def __init__(self):
        super().__init__('instagram')
        self._collection = self._database['need_publish']
    
    def get(self, name, start=None, end=None, ascending=None, **kwargs):
        request_result = self._collection.find({'name': name}, **kwargs)
        if ascending is not None:
            request_result.sort("date", 1 if ascending else -1) 
        start = start if isinstance(start, datetime) else datetime(1900, 1, 1)
        end = end if isinstance(end, datetime) else datetime.now()   
        for dict_items in request_result:
            serie = pd.Series(dict_items['data'])
            serie.index = pd.to_datetime(serie.index)
            yield serie.astype(float).loc[start:end]

    def publish(self, name, data, incr):
        date = data.index[-1]
        data.index = data.index.astype(str)
        incr = incr.rename_axis(['from', 'to']).reset_index()
        doc = {"date": date,
               "data" : data.rename(str).to_dict(),
               "incr": incr.rename(str).to_dict(),
               "status": "created"}
        self._collection.update_one({'name' : name, 'date' : date}, 
                                    {"$set" :doc},
                                    upsert=True)