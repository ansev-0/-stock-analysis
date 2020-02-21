from src.features_database.features_get.features_get import FeatureGet

class AlphavantageFeatureGet(FeatureGet):
    def __init__(self, collection):
        super().__init__(self, name_database='api_features', collection=collection, document_id='alphavantage')
