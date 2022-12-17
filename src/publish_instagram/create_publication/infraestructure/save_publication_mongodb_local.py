from src.database.database import DataBasePublishInstagram

class SavePublicationMongoDBLocal(DataBasePublishInstagram):
    
    def __init__(self):
        super().__init__('instagram')
        self._collection = self._database['need_publish']
    
    @DataBasePublishInstagram.try_and_wakeup
    def save(self, publication, path_local_image, data):
        return self._collection.update_one({'date': data['date'], 'name': data['name']},
                                           {'status': 'publication_created', 
                                            'url': publication.url,
                                            'path_local': path_local_image})
