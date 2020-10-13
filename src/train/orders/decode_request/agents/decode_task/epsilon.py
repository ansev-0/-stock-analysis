from src.train.rl_model.exploration.dynamic_epsilon import DynamicEpsilon

class DecodeEpsilonTask:
    def __call__(self, *args, **kwargs):
        return DynamicEpsilon()(*args, **kwargs)