from src.database.database import DataBase

class CheckToDataBase(DataBase):

    __NAMES_CHECK_DATABASE = ['database features', 'api features']
    def __init__(self, name, collection):
        if name not in  self.__NAMES_CHECK_DATABASE:
            raise ValueError(f'the databases supported by this class are: {self.__NAMES_CHECK_DATABASE}')

        super().__init__(name_database=name)
        self.collection = self.database[collection]

            


