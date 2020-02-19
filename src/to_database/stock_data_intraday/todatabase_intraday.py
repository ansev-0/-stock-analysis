from src.to_database.database import DataBase
from src.to_database.stock_data_intraday.errors.check_errors_save import CheckErrorsSaveInDataBase
class ToDataBaseIntraday(DataBase):

    __COMMON_NAME = 'stock_data_intraday_'

    def __init__(self, frecuency, new_database = 'create'):
        self.frecuency = frecuency
        self.check_save_base = CheckErrorsSaveInDataBase()
        self.check_save_base.check_parameter_create(create=new_database)
        if new_database == 'not create':
            self.check_save_base.check_frecuency_in_database(frecuency=frecuency)
        super().__init__(database_name=self.__COMMON_NAME + self.frecuency)

    def update_company_collection(self, list_dicts_to_update, company):

        collection = self.db[company]
        for dict_to_update in list_dicts_to_update:
            collection.update_one({'_id':dict_to_update['_id']},
                                  {'$set':dict_to_update['data']},
                                  upsert = True)