class SaveStockDataShowStatus:

    @staticmethod
    def notify_init_save_process():
        print(f'Starting acquisition process \n','_'*50)

    @staticmethod
    def notify_there_have_been_errors(companies):
        print(f'There have been errors in companies: \n{companies}')
    @staticmethod    

    def notify_try_again(attemp):
        print(f'Try again unsuccessful queries, attemp: {attemp} ')