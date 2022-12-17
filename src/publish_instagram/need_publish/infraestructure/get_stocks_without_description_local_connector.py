from src.database.database import DataBasePublishInstagram


class StocksWithoutDescriptions(DataBasePublishInstagram):

    def __init__(self):
        super().__init__('instagram')
        self._collection = self._database['need_publish']
        
    def get(self):
        return self._collection.find({'status': 'created'}, projection={'name' : 1, 
                                                                        'incr': 1, 
                                                                        'data': 1, 
                                                                        '_id': 0})
        
        