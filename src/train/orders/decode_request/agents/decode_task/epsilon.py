from src.dynamic_epsilon import DynamicEpsilon

class DecodeEpsilonTask:
    def __call__(self, *args, **kwargs):
        return DynamicEpsilon(*args, **kwargs)