from src.models.database.features.create import CreateFeaturesModel
from src.models.database.parameters.folder_of_folder_file import FolderofFolderExtFiles

class RegisterModel:

    def __init__(self, type_model, stock_name, *args, **kwargs):
        self._folder_of_folder = FolderofFolderExtFiles(type_model, stock_name, *args, **kwargs)
        self._register_in_db = CreateFeaturesModel(stock_name)

    @classmethod
    def agents(cls, stock_name, *args, **kwargs):
        return cls('agents', stock_name, *args, **kwargs)

    def __call__(self, keras_model):
        path = self._folder_of_folder.next_file
        keras_model.save(path)
        return path, self._register_in_db.from_keras_model(keras_model, path)
        