class SaveMany:
    def save(self, save_function, list_to_save):
        map(save_function, list_to_save)

    def save_and_return_errors(self, save_function, list_to_save):
        '''
        This function works with functions that return None when no errors occur.
        '''
        return {key : value 
                for key, value in zip(list_to_save,
                                      map(save_function, list_to_save))
                if value is not None}
