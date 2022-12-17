from src.database.database import DataBasePublishInstagram
import pandas as pd

class GetAllNeedPublishMongoDBLocal(DataBasePublishInstagram):
    
    def __init__(self):
        super().__init__('instagram')
        self._collection = self._database['need_publish']
    
    @DataBasePublishInstagram.try_and_wakeup
    def get(self, query):
        cursor = self._collection.find(query)
        #if cursor.count() == 0:
        #    return iter()
        
        for data in cursor:
            df = pd.DataFrame(data['data'])
            df.index = pd.to_datetime(df.index)
            yield {'data_image': {'dataframe': df, 
                                  'name': data['name'],
                                  'date': data['date']},
                   'caption': data['description']}
        