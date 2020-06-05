from functools import wraps
from src.train.keras.recurrent.fit_models.errors.fitmodel import CheckFitModelWithState
from src.tools.filter import filter_dict
from src.tools.filter import filter_valid_kwargs

class FitModelStateful:
    def __init__(self, model):
        self.model = model

    @classmethod
    def _fitmodel(cls, function):

        @wraps(function)
        def fit(self, x_train, y_train, epochs, not_reset_epochs, **kwargs):
            list_history = []
            for epoch in range(1, epochs + 1):
                print(f'Fitting {epoch}/{epochs}')
                modelfit = self.model.fit(x_train, y_train, **self.valid_kwargs(kwargs))
                output_func = function(self, modelfit, list_history, **kwargs)

                if epoch  not in not_reset_epochs:
                    self.model.reset_states()

            return output_func

        return fit
    
    
    def valid_kwargs(self, kwargs):
        valid_keys =  [key for key in self.model.fit.__code__.co_varnames[1:] 
                       if key not in ['window']]
        return filter_valid_kwargs(kwargs=kwargs,
                                   valid_keys=valid_keys)

class FitModelWithState(FitModelStateful):
    def __init__(self, model):
        super().__init__(model)


    @FitModelStateful._fitmodel
    def fit_keep_history(self, modelfit, list_history, history_keys=None, **kwargs):
 
        list_history.append(filter_dict(dictionary=modelfit.history,
                                        kfilter=history_keys))
        return list_history
        

    @FitModelStateful._fitmodel
    def only_fit(self, *args):
        return None
