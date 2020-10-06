from src.models.database.parameters.path import PathModels

class BasedOnTask:
    def __call__(self, based_on):
        return based_on if self._model_exist(based_on) \
                else False
                
    @staticmethod
    def _model_exist(model):
        return PathModels().path_exist(model)