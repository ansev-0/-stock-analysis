from src.database.database import DataBasePublishInstagram
import pandas as pd

class PublishDescription(DataBasePublishInstagram):
    
    def __init__(self):
        super().__init__('instagram')
        self._collection = self._database['need_publish']
        
    def publish_description(self, description, data):
        name = data['name']
        date = pd.to_datetime(pd.DataFrame(data['data']).index).max()
        return self._collection.update_one({"name": name, "date": date},
                                           {"$set": {'status': 'added_description',
                                            'description': description}})
        