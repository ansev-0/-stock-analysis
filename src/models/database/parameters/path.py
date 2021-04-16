import os
from src.tools.path import get_financial_path

class PathModels:
    
    path = os.path.abspath(os.path.join(get_financial_path(), 'models')) 
    os.makedirs(path, exist_ok=True)
    def path_folder(self, type_model, stock_name):
        os.makedirs(os.path.join(self.path, type_model), mode=0o777, exist_ok=True)

        path = os.path.join(self.path, type_model, stock_name)

        if not self.folder_exist(path):
            try:
                original_umask = os.umask(0o777)
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)

            finally:
                os.umask(original_umask)

        return path

    def folder_exist(self, path_folder):
        return os.path.isdir(path_folder)

    def file_exist(self, path_file):
        return os.path.isfile(path_file)




        