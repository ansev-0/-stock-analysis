from abc import ABCMeta, abstractproperty

class Menu(metaclass=ABCMeta):

    @abstractproperty
    def options_menu(self):
        pass

    @abstractproperty
    def switch_functions(self):
        pass

    def ask_for_selection(self, message):
        print(self.options_menu)
        return input(message)

    def run(self):
        selection = self.ask_for_selection(message='Enter One: ')
        while selection != 'quit':
            try:
                self.switch_functions[selection]()
            except Exception:
                selection = self.ask_for_selection(message='Please enter a valid one: ')
            else:
                selection = self.ask_for_selection(message='Enter One: ')