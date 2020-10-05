
from src.train.rl_model.learn.double_q_learning import LearnDoubleQlearning
from src.train.rl_model.play.double_q_learning import  PlayAndRememberDoubleQlearning, PlayValidationDoubleQlearning
from keras.models import load_model

class TrainAgentDoubleQlearning(LearnDoubleQlearning):

    def __init__(self, 
                 gamma,
                 epsilon_decay,
                 batch_learn_size, 
                 mem_size, 
                 file_model, 
                 interface_epoch_train=None, 
                 interface_epoch_validation = None):
        
        self._gamma = gamma
        self._interface_epoch_train = interface_epoch_train
        self._interface_epoch_validation = interface_epoch_validation
        self._mem_size = mem_size
        self._batch_learn_size = batch_learn_size
        self._epsilon_decay = epsilon_decay
        self._q_target = load_model(file_model)
        self._q_eval = load_model(file_model)
        self._agent_training = None
        self._agent_val = None
        self._validation_func = None

    @property
    def gamma(self):
        return self._gamma

    @property
    def mem_size(self):
        return self._mem_size

    @property
    def batch_learn_size(self):
        return self._batch_learn_size

    @property
    def epsilon_decay(self):
        return self._epsilon_decay

    @property
    def q_eval(self):
        return self._q_eval

    @property
    def q_target(self):
        return self._q_target

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
        #set validation func
        self._set_validation_func(validation_data, env_validation) 
        # do epochs
        self._epochs(self, epochs, sort, replace, freq_update, validation_random, *args, **kwargs)
        #reset agent
        self._reset_agent()

    def _epochs(self, epochs, sort, replace, freq_update, validation_random, *args, **kwargs):
        for epoch in range(1, epochs+1):  
            #train epoch
            self._train(self.epsilon_decay.epsilon, 
                        sort, 
                        replace, 
                        *args, 
                        **kwargs)
            #update q network target
            if (epoch-1) % freq_update == 0:
                self.update_q_target() 

            #validation epoch
            self._validation_func(self.epsilon_decay.epsilon 
                                  if validation_random else 1)               
            self._epsilon_decay.step()

    def _reset_agent(self):
        self._agent_training = None
        self._agent_validation = None
        self._validation_func = None

    def _train(self, random_probability, sort, replace, *args, **kwargs):
        #agent play
        self._agent_training.play(random_probability)
        # replay sample of experience
        memory = self._agent_training.memory.sample_buffer(self._batch_learn_size,
                                                           sort=sort, 
                                                           replace=replace)
        memory = self._tuple_mem_features(memory)
        # agent learn
        result_fit = self.learn(memory, *args, **kwargs)
        try:
            self._interface_epoch_train.get(self._q_eval,
                                            self._agent_training.env,
                                            self._agent_training.states_env,
                                            result_fit)
        except Exception: 
            pass

    def _validation(self, *args):
        self._validation_agent.play(*args)
        try:
            self._interface_epoch_validation.get(self._q_eval,
                                                 self._validation_agent.env,
                                                 self._validation_agent.states_env)
        except Exception:
            pass

    def _set_validation_func(self, validation_data, env_validation):
        if validation_data is not None and env_validation is not None:
            self._validation_agent = PlayValidationDoubleQlearning(q_eval=self.q_eval, 
                                                                   env=env_validation, 
                                                                   states_price=validation_data)
            self._validation_func = self._validation
        self._validation_func = lambda probability, *args, **kwargs: None

    @staticmethod
    def _tuple_mem_features(memory):
        return tuple(list(mem.values()) if isinstance(mem, dict) 
                     else mem 
                     for mem in memory)
