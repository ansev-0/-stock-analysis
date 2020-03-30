class AlphaVantageShowStatus:

    @staticmethod
    def notify_try_connect():
        print(f'trying connect with API Alphavantage')

    @staticmethod
    def notify_request_exception(error):
      print(f'Request exception: \n {error}')

    @staticmethod
    def notify_error_format(error):
        print('Invalid format received: \n', error)
    @staticmethod
    def notify_sleeping(delay):
        print(f'Waiting {delay} seconds for new attemp\n')

    @staticmethod
    def notify_json_received_succesfully():
        print('json received successfully')

    
    