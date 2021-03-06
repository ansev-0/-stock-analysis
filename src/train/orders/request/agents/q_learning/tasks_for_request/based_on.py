from src.models.database.parameters.path import PathModels

class BasedOnTask:
    
    def __call__(self, path):
        if not PathModels().file_exist(path):
            raise ValueError('Invalid path, not model found')
        return path
