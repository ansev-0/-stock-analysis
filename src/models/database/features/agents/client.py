from src.database.database import DataBaseAdminModels

class DataBaseFeatureModels(DataBaseAdminModels):

    def __init__(self, stock_name):
        super().__init__('model_features')
        self._collection = self._database[stock_name]

    @property
    def list_stock_models(self, **kwargs):
        return self._database.list_collection_names(**kwargs)

    @property
    def collection(self):
        return self._collection

