from src.view.acquisition.to_database.show_status.status_save_data import SaveDataShowStatus

class SaveForexDataShowStatus(SaveDataShowStatus):

    @staticmethod
    def notify_there_have_been_errors(list_queries):
        list_quieres = list(map('_TO_'.join, list_queries))
        print(f'There have been errors in pair queries: \n{list_quieres}')

