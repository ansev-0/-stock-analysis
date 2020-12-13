from src.train.rl_model.exploration import epsilon

class DynamicEpsilon:
    def __call__(self, function, parameters):
        return getattr(epsilon, function)(**parameters)
