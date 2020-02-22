from src.features_database.features_get.features_get import FeatureGet

class DataBasesFeatureGet(FeatureGet):
    def __init__(self, collection, document_id):
        super().__init__(name_database='api_features', collection=collection, document_id=document_id)
