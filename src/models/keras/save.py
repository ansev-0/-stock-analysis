from src.models.path import PathModel

class SaveFinancialWorksModel:
    def __init__(self, name_model, model):
        model.save(PathModel()(name_model))


