from src.dtaabase.database import DataBaseAdminModelFeatures

class DataBaseModelFeatures(DataBaseAdminModelFeatures):
    def __init__(self):
        super().__init__('model_features')