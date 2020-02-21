from src.features_database.features_records.feature_records import FeatureRecords

class AlphavantageFeatureRecords(FeatureRecords):
    def __init__(self, collection, document_id):
        super().__init__(self, name_database='database_features', collection=collection, document_id=document_id)
