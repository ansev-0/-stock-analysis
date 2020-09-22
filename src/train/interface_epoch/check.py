from src.portfolio.state import StatePortfolio
from src.model_environment.run.run import RunEnv
from keras.models import Model

class CheckInterfaceInputs:

    @staticmethod
    def _is_keras_model(model):
        if not isinstance(model, Model):
            raise ValueError(f'{model} is not an instance of {Model}')

    @staticmethod
    def _is_env_states(env_states):
        if not isinstance(env_states, StatePortfolio):
            raise ValueError(f'{env_states} is not an instance of {StatePortfolio)}')

    @staticmethod
    def _is_run_env(run_env):
        if not isinstance(run_env, RunEnv):
            raise ValueError(f'{run_env} is not an instance of {Model}')

