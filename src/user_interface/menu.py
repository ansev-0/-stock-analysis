class Menu:

    def __init__(self, options_menu, switch_functions):
        self.options_menu = options_menu
        self.switch_functions = switch_functions

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