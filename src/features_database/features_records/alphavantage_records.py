from src.features_database.features_records.feature_records import FeatureRecords

class AlphavantageFeatureRecords(FeatureRecords):
    def __init__(self, collection):
        super().__init__(self, name_database='api_features', collection=collection, document_id='alphavantage')
