from src.models.database.parameters.folder_of_folder_file import FolderofFolderExtFiles
from keras.models import Model, load_model
import os

class PathTask:
    def __call__(self, stock_name, based_on):
        folder = FolderofFolderExtFiles.agents(stock_name)
        path = folder.next_file
        model = load_model(based_on).save(path)
        return path

    def remove(self, path):
        return os.remove(path)