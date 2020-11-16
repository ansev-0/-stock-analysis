class SaveDataShowStatus:

    @staticmethod
    def notify_init_save_process():
        print(f'Starting acquisition process \n','_'*50)
        
    @staticmethod
    def notify_try_again(attemp):
        print(f'Try again unsuccessful queries, attemp: {attemp} ')