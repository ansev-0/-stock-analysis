from src.assets.database.database import AssetsDatabase
from src.assets.asset import Asset

class FindAssetInDataBase(AssetsDatabase):

    def one(self, return_asset, *args, **kwargs):
        result = self._collection.find_one(*args, **kwargs)
        if not isinstance(result, dict):
            return None
        return self._find_one_output(result, return_asset)

    def many(self, return_asset, *args, **kwargs):
        return [Asset(**self._filter_id(result)) 
                for result in self._collection.find(*args, **kwargs)]\
        if return_asset else self._collection.find(*args, **kwargs)

    def find_label(self, label, return_asset, **kwargs):
        return self._find_one_by_tag('label', label, return_asset, **kwargs)

    def find_name(self, name, return_asset, **kwargs):
        return self._find_one_by_tag('name', name, return_asset, **kwargs)

    def _find_one_by_tag(self, tag, tag_value, return_asset, **kwargs):
        result = self._collection.find_one({tag : tag_value}, **kwargs)
        if not result:
            return None
        return self._find_one_output(result, return_asset)

    def _find_one_output(self, result, return_asset):
        return Asset(**self._filter_id(result)) \
            if return_asset else result

    @staticmethod
    def _filter_id(result):
        return {key : value for key, value in result.items() 
                if key != '_id'}

