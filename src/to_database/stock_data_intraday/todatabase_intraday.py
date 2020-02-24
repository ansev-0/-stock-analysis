from src.database.database import DataBase
from src.to_database.stock_data_intraday.errors.check_errors_save.check_errors_save \
    import CheckErrorsSaveInDataBase
from src.acquisition_incidents.incidents import AcquisitionIncidents

class ToDataBaseIntraday(DataBase):

    __COMMON_NAME = 'stock_data_intraday_'

    def __init__(self, frecuency, new_database='create'):
        self._frecuency = frecuency
        self.check_save_base = CheckErrorsSaveInDataBase(frecuency=self._frecuency)
        self.check_save_base.check_parameter_create(create=new_database)
        self.incidents = AcquisitionIncidents()

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
    def report_incident(self, api, tuple_error):
        self.incidents.report(api=api,
                              **dict(zip(self.incidents.report.__code__.co_varnames[-2:],
                                     tuple_error)))
    

