from ast import literal_eval

class Input:
    def get_dict(self):
        return self.__get_and_check_input(dict)

    def get_list(self):
        return self.__get_and_check_input(list)

    def get_tuple(self):
        return self.__get_and_check_input(tuple)

    def get_set(self):
        return self.__get_and_check_input(set)
    
    def __get_and_check_input(self, type_correct):
        
        input_user = literal_eval(self.__get_input(type_correct))
        self.__eval_input(type_correct, input_user)
        return input_user

    @staticmethod
    def __eval_input(type_correct, input_user):
        if not isinstance(input_user, type_correct):
            raise ValueError(f'{input_user} is invalid input for type {type_correct.__name__}')
    @staticmethod
    def __get_input(type_correct):
        return input(f'Please enter input of type {type_correct}: ')

