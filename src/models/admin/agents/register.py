from src.models.database.features.agents.create import CreateFeaturesModel
from src.models.database.parameters.folder_of_folder_file import FolderofFolderExtFiles

class RegisterAgent:

    def __init__(self, stock_name, *args, **kwargs):

        self._folder_of_folder = FolderofFolderExtFiles.agents(stock_name, 
                                                               *args, 
                                                               **kwargs)
                                                        
        self._register_in_db = CreateFeaturesModel(stock_name)

    def __call__(self, keras_model):

        path = self._folder_of_folder.next_file
        keras_model.save(path)
        return path, self._register_in_db.from_keras_model(keras_model, path)

