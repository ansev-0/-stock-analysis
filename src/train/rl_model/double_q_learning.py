
from src.train.rl_model.learn.double_q_learning import LearnDoubleQlearning
from src.train.rl_model.play.double_q_learning import  PlayAndRememberDoubleQlearning, PlayValidationDoubleQlearning
from keras.models import load_model

class TrainAgentDoubleQlearning(LearnDoubleQlearning):

    def __init__(self, 
                 gamma,
                 epsilon_decay,
                 batch_train_size, 
                 mem_size, 
                 file_model, 
                 model=None, 
                 load_exist=True, 
                 interface_epoch_train=None, 
                 interface_epoch_validation = None):
        
        self._gamma = gamma
        self._interface_epoch_train = interface_epoch_train
        self._interface_epcoh_validation = interface_epoch_validation
        self._mem_size = mem_size
        self._batch_train_size = batch_train_size
        self._epsilon_decay = epsilon_decay
        self._agent_training = None
        self._agent_val = None
        self._q_target = None
        self._q_eval = None
        self._get_model(model, file_model, load_exist)
        
    @property
    def gamma(self):
        return self._gamma

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


    def _get_model(self, model, file_model, load_exist):
        if load_exist:
            self._q_eval = load_model(file_model) 
            self._q_target = load_model(file_model)
        else:
            self._q_eval = model
            # q_target is a copy of q_eval
            self._q_eval.save(file_model)
            self._q_target = load_model(file_model)

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
        validation_func = self._validation_func(validation_data, env_validation) 

        for epoch in range(1, epochs+1):  
            #train epoch
            fit_result = self._train(self.epsilon_decay.epsilon, 
                                     epoch, 
                                     freq_update, 
                                     sort, 
                                     replace, 
                                     *args, 
                                     **kwargs)
            #validation epoch
            validation_func(self.epsilon_decay_epsilon if validation_random else 1)
            self._epsilon_decay.step()
        #reset agent
        self._reset_agent()

    def _reset_agent(self):
        self._agent_training = None
        self._agent_validation = None

    def _train(self, random_probability, epoch, freq_update, sort, replace, *args, **kwargs):

        self._agent_training.play(random_probability)
        memory = self._agent_training.memory.sample_buffer(self._batch_train_size,
                                                           sort=sort, 
                                                           replace=replace)
        memory = tuple(list(mem.values()) if isinstance(mem, dict) else mem 
                       for mem in memory)
        result_fit = self.learn_and_update_q_target(memory, *args, **kwargs) if (epoch-1) % freq_update == 0 \
                     else self.learn(memory, *args, **kwargs)
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
                                                 self._agent_validation.env,
                                                 self._agent_validaiton.states_env)
        except Exception:
            pass

    def _validation_func(self, validation_data, env_validation):
        if validation_data is not None and env_validation is not None:
            self._validation_agent = PlayValidationDoubleQlearning(q_eval=self.q_eval, 
                                                                   env=env_validation, 
                                                                   states_price=validation_data)
            return self._validation
        return lambda probability, *args, **kwargs: None





