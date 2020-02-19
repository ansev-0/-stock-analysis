from src.to_database.database import DataBase

class CheckToDataBase(DataBase):
    __NAME_CHECK_DATABASE = 'check_todatabase'
    def __init__(self):
        super().__init__(name_database=self.__NAME_CHECK_DATABASE)

