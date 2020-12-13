from src.models.database.parameters.folder_file_parameters import FolderProperties
import os

class FolderExtFiles(FolderProperties):
    
    @property
    def next_file(self):
        
        path_file = self.name_next_element
        file_path = os.path.join(self.path, path_file)
        file = open(file_path, 'w')
        file.close()
        
        return path_file