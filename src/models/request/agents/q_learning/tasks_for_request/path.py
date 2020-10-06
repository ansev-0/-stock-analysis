from src.models.database.parameters.folder_of_folder_file import FolderofFolderExtFiles

class PathTask:
    def __call__(self, stock_name):
        folder = FolderofFolderExtFiles.agents(stock_name)
        return folder.next_file