import os

class PathModels:
    
    path = os.path.abspath('/home/antonio/financialworks/models') 

    def path_folder(self, type_model, stock_name):
        path = os.path.join(self.path, type_model, stock_name)

        if not self.folder_exist(path):
            try:
                original_umask = os.umask(0o777)
                os.makedirs(path)
                os.chmod(path, 0o777)

            finally:
                os.umask(original_umask)

        return path

    def folder_exist(self, path_folder):
        return os.path.isdir(path_folder)

    def file_exist(self, path_file):
        return os.path.isfile(path_file)




        