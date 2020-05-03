from src.exceptions.train_exceptions import ModelFitError
class CheckFitModelWithState:
    @staticmethod
    def check_history_keys(history_keys):
        try:
            iter(history_keys)
        except TypeError:
            raise   ModelFitError('You must pass a iter')

