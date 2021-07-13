from src.acquisition.to_database.tiingo.saver import SaverTiingo

class SaverTiingoNews(SaverTiingo):
    tiingo_db = 'tiingo_news'

    def __call__(self, response_to_db, where_save):
        for collection in where_save:
            self.collection = collection
            self.update_one({'$set' : response_to_db}, upsert=True)
