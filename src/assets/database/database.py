from src.database.database import DataBaseAdminAssets
from src.assets.asset import Asset

class AssetsDatabase(DataBaseAdminAssets):
    
    def __init__(self):
        super().__init__('assets')
        self._collection = self._database['basic']

    def list_assets_labels(self, **kwargs):
        return self._database.list_collection_names(**kwargs)

    def _raise_if_not_asset(self, asset):
        if not self._is_asset(asset):
            raise TypeError('You must pass asset instance')

    @staticmethod
    def _is_asset(asset):
        return isinstance(asset, Asset)



    



