class ReaderShowStatus:
    @staticmethod
    def notify_try_connect(query):
        print(f'making request, query: \n {query}')
    @staticmethod
    def notify_not_error():
        print('not requests exceptions')
    @staticmethod
    def notify_error():
                print('there has been an exception using requests.get')


    
    