from src.database.database import DataBaseAdminTwitterRequests

class UpdateSearchAsset(DataBaseAdminTwitterRequests):

    def __init__(self, collection):
        super().__init__('twitter_search_assets')
        self._collection = self._database[collection]

    @property
    def collection(self):
        return self._collection

    @DataBaseAdminTwitterRequests.try_and_wakeup
    def one(self, _id, dict_to_update):
        return self._collection.update_one({'_id' : _id}, 
                                           self._update_dict(dict_to_update), 
                                           upsert=True)

    def _update_dict(self, dict_to_update):
        return {'$set' : dict_to_update}
