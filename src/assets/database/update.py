from src.assets.database.database import AssetsDatabase

class UpdateAssetInDataBase(AssetsDatabase):

    _UPDATE_KEYS = ('label', 'name')

    def one(self, asset, **kwargs):

        key_words = asset.key_words if self._is_asset(asset) else asset
        where = self._get_where_one(key_words)
        return self._collection.update_one(where, 
                                           self._build_set(key_words), 
                                           **kwargs)

    def many(self, *args, **kwargs):
        return self._collection.update_many(*args, **kwargs)

    @staticmethod
    def _build_set(dict_to_update):
        return {'$set' : dict_to_update}

    def _get_where_one(self, key_words):
        return {key : key_words[key] 
                for key in self._UPDATE_KEYS 
                if key in key_words}
