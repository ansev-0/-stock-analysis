from abc import ABCMeta, abstractmethod

class SaveMany:
    
    def save(self, save_function, list_to_save):
        map(lambda arg: save_function(*arg) if isinstance(arg, tuple) else save_function(arg), 
            list_to_save)

    def save_and_return_errors(self, save_function, list_to_save):
        '''
        This function works with functions that return None when no errors occur.
        '''
        return {key : value 
                for key, value in zip(list_to_save,
                                      map(lambda arg: save_function(*arg) if isinstance(arg, tuple) \
                                          else save_function(arg),
                                          list_to_save)
                                     )
                if value is not None}



class UpdateManyStockData(metaclass=ABCMeta):

    __save_many=SaveMany()

    @abstractmethod
    def to_database(self):
         pass
    
    def to_database_getting_errors(self, list_company):
        return self.__save_many.save_and_return_errors(self.to_database, list_company)

    def to_database_ignoring_errors(self, list_company):
        return self.__save_many.save(self.to_database, list_company)