class AlphaVantageStatus:

    @staticmethod
    def notify_try_connect(query):
        print(f'trying connect with API Alphavantage, query: \n {query}')

    @staticmethod
    def notify_request_exception(error):
      print(f'Request exception: \n {error}')

    @staticmethod
    def notify_error_format(error):
        print('Invalid format received: \n', error)
    @staticmethod
    def notify_sleeping(delay):
        print(f'Waiting {delay} for new attemp ')

    @staticmethod
    def notify_json_received_succesfully():
        print('json received successfully')

    
    