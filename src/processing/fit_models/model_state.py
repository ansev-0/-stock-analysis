class FitModelWithState:
    def __init__(self, model, x_train, y_train):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train

    def fit(self, epochs, reset_epochs=None, history_keys=None, **kwargs):

        history_list = []
        output_func = self.__history_output_func(history_keys)
        for epoch in range(1, epochs + 1):
            history = self.model.fit(self.x_train, self.y_train, **kwargs)
            output_func(history, history_list)
            if (epoch is reset_epochs) or (epoch in reset_epochs):
                self.model.reset_states()

        if history_list:
            return history_list
        return None

    @staticmethod
    def __history_output_func(history_keys):
        try:
            iter(history_keys)
            if len(history_keys) == 1:
                return lambda history, list_history: list_history.append(
                    dict(filter(lambda item: item[0] is history_keys,
                                history.items())))
      
            return lambda history, list_history: list_history.append(
                dict(filter(lambda item: item[0] in history_keys,
                            history.items())))
        except TypeError:
            return lambda *args, **kwargs: None
