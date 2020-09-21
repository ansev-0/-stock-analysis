
from src.train.rl_model.learn.double_q_learning import LearnDoubleQlearning
from src.train.rl_model.play.double_q_learning import  PlayAndRememberDoubleQlearning, PlayValidationDoubleQlearning
from keras.models import load_model


class TrainAgentDoubleQlearning(LearnDoubleQlearning):

    def __init__(self, epsilon_decay,
                 batch_train_size, 
                 mem_size, 
                 model=None, 
                 file_model=None, 
                 load_model=True, 
                 interface_epoch_train=None, 
                 interface_epoch_validation = None):

        self._interface_epoch_train = interface_epoch_train
        self._interface_epcoh_validation = interface_epoch_validation
        self._mem_size = mem_size
        self._batch_train_size = batch_train_size
        self._epsilon_decay = epsilon_decay
        self._agent_training = None
        self._agent_val = None
        self._q_target = None
        self._q_eval = None
        self._get_model()

    @property
    def mem_size(self):
        return self._mem_size

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def epsilon_decay(self):
        return self._epsilon_decay

    @property
    def q_eval(self):
        return self._q_eval

    @property
    def q_target(self):
        return self._q_target
        

    @classmethod
    def with_model(cls, file_model):
        return cls(None, file_model, True)

    @classmethod
    def new_model(cls, model, file_model):
        return cls(model, file_model, False)


    def _get_model(self, model=None, file_model=None, load_model=True):
        self._q_eval = load_model(file_model) if load_model else model
        self._q_target = self._q_eval

    def train(self, 
              epochs,
              train_data, 
              env_train, 
              validation_data=None, 
              env_validation=None, 
              freq_update=1, 
              sort=True,
              replace=False,
              validation_random=False,
              *args, 
              **kwargs):

        self._epsilon_decay.reset()
        self._agent_training = PlayAndRememberDoubleQlearning(mem_size=self._mem_size, 
                                                               q_eval=self.q_eval, env=env_train,
                                                               states_price=train_data)
        validation_func = self._validation_func(validation_data, env_validation) 

        for epoch in range(1, epochs+1):  
            
            print(f'Epoch : {epoch}')
            #train epoch
            fit_result = self._train(self.epsilon_decay.epsilon, epoch, freq_update, sort, replace)
            #validation epoch
            validation_func(self.epsilon_decay_epsilon if validation_random else 1)
            self._epsilon_decay.step()

        self._reset_agent()


    def _reset_agent(self):
        self._agent_training = None
        self._agent_validation = None


    def _train(self, random_probability, epoch, freq_update, sort, replace, *args, **kwargs):
        self._agent_training.play(random_probability)
        memory = self._agent_training.memory.sample_buffer(self._batch_train_size,
                                                           sort=sort, 
                                                           replace=replace)
        memory[0] = list(memory[0].values())
        memory[3] = list(memory[3].values())

        result_fit = self.learn_and_update_q_target(memory, *args, **kwargs) if (epoch-1) % freq_update == 0 \
                     else self.learn(memory, *args, **kwargs)

        try:
            self._interface_epoch_train.push(self._agent_training.env,
                                             self._agent_training.states_env,
                                             result_fit)
        except Exception:
            pass

def _validation(self, *args):

    self._validation_agent.play(*args)
    try:
        self._interface_epcoh_validation.push(self._agent_validation.env,
                                              self._agent_validaiton.states_env)
    except Exception:
        pass

def _validation_func(self, validation_data, env_validation):
    if validation_data is not None and env_validation is not None:
        self._validation_agent = PlayValidationDoubleQlearning(q_eval=self.q_eval, 
                                                               env=env_validation, 
                                                               states_prices=validation_data)
        return 
    return lambda validation, data, env_validation, *args, **kwargs: None





