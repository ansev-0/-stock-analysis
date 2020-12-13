from src.view.acquisition.to_database.show_status.status_save_data import SaveDataShowStatus

class SaveFinancialDataShowStatus(SaveDataShowStatus):

    @staticmethod
    def notify_there_have_been_errors(companies):
        print(f'There have been errors in companies: \n{companies}')

