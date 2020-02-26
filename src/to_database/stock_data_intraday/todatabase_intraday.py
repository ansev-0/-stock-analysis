from src.database.database import DataBase
from src.to_database.stock_data_intraday.errors.check_to_database \
    import CheckErrorsToDataBase


class ToDataBaseIntraday(DataBase):

    __COMMON_NAME = 'stock_data_intraday_'

    def __init__(self, frecuency, new_database='create'):
        self._frecuency = frecuency
        self.check_save_base = CheckErrorsToDataBase(frecuency=self._frecuency)
        self.check_save_base.check_parameter_create(create=new_database)

        if new_database == 'not create':
            self.check_save_base.check_frecuency_in_database()
        super().__init__(name_database=self.__COMMON_NAME + self._frecuency)

    def update_stock_data(self, list_dicts_to_update, company, **kwards):
        collection = self.database[company]
        for dict_to_update in list_dicts_to_update:
            collection.update_one({'_id' : dict_to_update['_id']},
                                  {'$set' : dict_to_update['data']},
                                  upsert=True,
                                  **kwards)


