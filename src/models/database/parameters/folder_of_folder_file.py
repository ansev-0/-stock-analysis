from src.models.database.parameters.folder_file_parameters import FolderProperties
from src.models.database.parameters.folder_ext_files import FolderExtFiles
from src.models.database.parameters.path import PathModels
import os

class FolderofFolderExtFiles(FolderProperties):
    
    def __init__(self, type_model, stock_name, ext_files='.h5', limit_mb=10e8):

        super().__init__(PathModels().path_folder(type_model, stock_name),
                         stock_name, 
                         '')

        self._ext_files = ext_files
        self._base_file_name = stock_name
        self._limit_mb = limit_mb

    @classmethod 
    def agents(cls, stock_name, limit_mb=10e8):
        return cls('agents', stock_name, limit_mb=limit_mb)


    @property
    def limit_mb(self):
        return self._limit_mb
        
    @property
    def base_file_name(self):
        return self._base_file_name

    @property
    def ext_files(self):
        return self._ext_files
    
    @property
    def folders_obj(self):
        return list(map(self._folder_obj, self.elements))
    
    @property
    def next_file(self):
        not_complete_folder_obj = self._get_not_complete_folder_obj()
        
        if not not_complete_folder_obj:
            self._new_folder()
            return self._get_not_complete_folder_obj().next_file  
            
        return not_complete_folder_obj.next_file
    
        
    def _folder_obj(self, folder):
        return FolderExtFiles(path=os.path.join(self.path, folder),
                              base_name=self.base_file_name,
                              ext=self.ext_files)
    
    def _get_not_complete_folder_obj(self):
        not_complete_folders = list(filter(lambda obj: obj.total_size < self._limit_mb,
                                           self.folders_obj))
        
        if len(not_complete_folders) > 1:
            raise ValueError('Files have been improperly modified')
                
        return not_complete_folders[0] if not_complete_folders else None
    
    def _new_folder(self):
        os.makedirs(os.path.join(self.path, self.name_next_element))
