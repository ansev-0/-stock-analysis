from src.assets.database.database import AssetsDatabase

class CreateAssetInDataBase(AssetsDatabase):

    @AssetsDatabase.try_and_wakeup
    def one(self, asset):
        return self._collection.insert_one(asset.key_words 
                                           if self._is_asset(asset) 
                                           else asset)
    @AssetsDatabase.try_and_wakeup
    def many(self, assets):
        return self._collection.insert_many([asset.key_words if self._is_asset(asset)
                                             else asset
                                             for asset in assets])

#from src.assets.asset import assets
#CreateAssetInDataBase().many(assets)
