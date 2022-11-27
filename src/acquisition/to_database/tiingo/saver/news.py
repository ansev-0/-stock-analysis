from src.acquisition.to_database.tiingo.saver.saver import SaverTiingo
from collections import defaultdict
from src.assets.database.find import FindAssetInDataBase

class SaverTiingoNews(SaverTiingo):

    tiingo_db = 'tiingo_news'
    assets = list(map(lambda x: x['label'].lower(), FindAssetInDataBase().many(False, {})))

    def __call__(self, response_to_db, where_save):
        dict_to_save_by_collection = defaultdict(dict)
        for json_dict, list_save in zip(response_to_db, where_save):
            for collection in filter(lambda ticker: ticker.lower() in self.assets, list_save):
                dict_to_save_by_collection[collection].update(json_dict)

        for collection, json_to_db in dict_to_save_by_collection.items():
            self.collection = collection
            self.update_one({'_id' : json_to_db['_id']},
                            {'$set' : json_to_db}, 
                            upsert=True)


class SaverTiingoNewsFromDataFrame(SaverTiingo):

    tiingo_db = 'tiingo_news'
    assets = list(map(lambda x: x['label'].lower(), FindAssetInDataBase().many(False, {})))

    def __call__(self, list_json_to_db, collection):
        if collection.lower() not in self.assets:
            return None
        self.collection = collection
        for json_to_db in list_json_to_db:
            self.update_one({'_id' : json_to_db['_id']},
                            {'$set' : json_to_db}, 
                            upsert=True)
        return True


