from src.train.orders.decode_request.agents.decode_task.create_builder import CreateBuilderTask
from src.train.orders.decode_request.agents.decode_task.data import DecodeDataTask
from src.train.orders.decode_request.agents.decode_task.data import DecodeForexDataTask
from src.train.orders.decode_request.agents.decode_task.reward import DecodeRewardTask
from src.train.orders.decode_request.agents.decode_task.states_actions import DecodeStatesActionsTask
from src.model_environment.run.run_q_learning import RunEnvAdaptQlearningModel
from src.train.orders.decode_request.agents.decode_task.actions import DecodeActionsTask
from src.train.orders.decode_request.agents.decode_task.conf_build_agent import DecodeConfBuildAgentTask
from src.train.rl_model.double_q_learning import TrainAgentDoubleQlearning
from src.tools.mongodb import decode_array_from_mongodb

class DecodeOrder:
    
    _create_builder = CreateBuilderTask()
    _decoder_data = DecodeDataTask()
    _decoder_forex_data = DecodeForexDataTask()
    _decoder_states_actions = DecodeStatesActionsTask()
    _decoder_actions = DecodeActionsTask()
    _decoder_conf_agent = DecodeConfBuildAgentTask()
    _decoder_reward = DecodeRewardTask()

    def __call__(self, order_dict):
        train_params = {}
        #get tensor
        (train_params['train_data'], train_params['validation_data'], 
         train_params['train_commision'], train_params['validation_commision']) = self._decode_data(order_dict)

        # create builder
        builder_train = self._create_builder(order_dict['broker'], 
                                             order_dict['cache_id_commision_train'], 
                                             order_dict['cache_id_train'])
        builder_validation = self._create_builder(order_dict['broker'], 
                                            order_dict['cache_id_commision_validation'], 
                                            order_dict['cache_id_validation'])
        # get rewards
        reward_done, reward_not_done = self._decode_reward(order_dict, builder_train)
        # get sim states action
        train_states_actions, validation_states_actions = self._decode_states_actions(order_dict, builder_train, builder_validation)
        adapter = self._decode_actions(order_dict)
        #build run env
        train_params['env_train'] = self._decode_run_env(adapter, train_states_actions, reward_done, reward_not_done)
        train_params['env_validation'] = self._decode_run_env(adapter,
                                                              validation_states_actions,
                                                              reward_done, 
                                                              reward_not_done) \
            if train_params['validation_data'] is not None else None
        
        #return agent and params to call train function
        return lambda: self._decode_conf_agent(order_dict).train(**train_params, **order_dict['conf_call_agent'])

    def _decode_data(self, order_dict):

        train_sequences = self._decoder_data(order_dict['cache_id_train'])
        train_commision_sequences = self._decoder_forex_data(order_dict['cache_id_commision_train'])
            
        try:
            validation_sequences = self._decoder_data(order_dict['cache_id_validation'])
        except KeyError:
            validation_sequences = None
        try:
            validation_commision_sequences = self._decoder_forex_data(order_dict['cache_id_commision_validation'])
        except KeyError:
            validation_commision_sequences = None


        return train_sequences, validation_sequences, train_commision_sequences, validation_commision_sequences

    def _decode_reward(self, order_dict, builder_train):
        return self._decoder_reward(order_dict['rewards'], builder_train), \
            self._decoder_reward(order_dict['rewards_not_done'], builder_train)


    def _decode_states_actions(self, order_dict, builder_train, builder_validation):
        train_states_actions = self._decoder_states_actions(order_dict['train_states_actions'], 
                                                            builder_train) 

        try:
            validation_states_actions = self._decoder_states_actions(order_dict['validation_states_actions'], 
                                                                     builder_validation)
        except KeyError:
            validation_states_actions = None

        return train_states_actions, validation_states_actions

    def _decode_run_env(self, 
                        adapter, 
                        states_actions, 
                        reward_action_done, 
                        reward_action_not_done):

        return RunEnvAdaptQlearningModel(adapter=adapter,
                                         states_actions=states_actions, 
                                         reward_action_done=reward_action_done, 
                                         reward_action_not_done=reward_action_not_done)

    def _decode_actions(self, order_dict):
        return self._decoder_actions(order_dict['actions'])
        
    def _decode_conf_agent(self, order_dict):
        return TrainAgentDoubleQlearning(file_model=order_dict['path'], 
                                         **self._decoder_conf_agent(order_dict['conf_build_agent']))
