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
            request_result.sort("_id", 1 if ascending else -1) 
        start = start if isinstance(start, datetime) else datetime(1900, 1, 1)
        end = start if isinstance(start, datetime) else datetime.now()   
        for dict_items in request_result:
            df = pd.DataFrame(dict_items['data'])
            df.index = pd.to_datetime(df.index)
            yield df.astype(float).loc[start:end]

    def publish(self, name, data):
        self._collection.update_one({'name' : name, '_id' : data.index[-1]}, 
                                    {"$set" :{"data" : data.astype(str).to_dict("index"),
                                              "status": "created"}},
                                    upsert=True)