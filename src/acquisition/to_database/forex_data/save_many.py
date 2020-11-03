class SaveMany:

    def save(self, save_function, list_tuple_to_save):
        map(lambda tup: save_function(*tup),
            list_tuple_to_save)

    def save_and_return_errors(self, save_function, list_tuple_to_save):
        '''
        This function works with functions that return None when no errors occur.
        '''
        return {'_TO_'.join(tup_to_save) : value 
                for tup_to_save, value in zip(list_tuple_to_save,
                                              map(lambda tup: save_function(*tup),
                                                  list_tuple_to_save)
                                             )
                if value is not None}
