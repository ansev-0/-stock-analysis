from src.train.orders.decode_request.decode_task.stock_data import DecodeStockDataTask
from src.model_environment.rewards.dynamic.reward import BuilderReward
from src.train.orders.decode_request.decode_task.reward import DecodeRewardTask
from src.train.orders.decode_request.decode_task.states_actions import DecodeStatesActionTask
from src.model_environment.run.run_q_learning import RunEnvAdaptQlearningModel
from src.train.orders.decode_request.decode_task.actions import DecodeActionsTask

class DecodeOrder:

    _decoder_stock_data = DecodeStockDataTask()
    _decoder_reward = DecodeRewardTask()
    _decoder_states_actions = DecodeStatesActionTask()
    _decoder_actions = DecodeActionsTask()

    def __call__(self, order_dict):
        #get tensor
        train_sequences, validation_sequences = self._decode_stock_data(order_dict)
        # get reards in env
        reward_done, reward_not_done = self._decode_reward(order_dict)
        # get sim states action
        train_states_actions, validation_states_actions = self._decode_states_actions(order_dict)
        adapter = self._decode_actions(order_dict)
        #build run env
        run_env_train = self._decode_run_env(adapter, train_states_actions, reward_done, reward_not_done)
        if validation_sequences is not None:
            run_env_validation = self._decode_run_env(adapter, validation_states_actions, reward_done, reward_not_done)
        else:
            run_env_validation = None

    def _decode_stock_data(self, order_dict):

        train_sequences = self._decoder_stock_data(order_dict['cache_id_train'])['sequences']

        try:
            validation_sequences = self._decoder_stock_data(order_dict['cache_id_validation'])['sequences']
        except KeyError:
            validation_sequences = None

        return train_sequences, validation_sequences

    def _decode_reward(self, order_dict):
        return self._decoder_reward(order_dict['rewards']), self._decoder_reward(order_dict['rewards_not_done'])


    def _decode_states_actions(self, order_dict):
        train_states_actions = self._decoder_states_actions(order_dict['train_states_actions'])
        try:
            validation_states_actions = self._decoder_states_actions(order_dict['validation_states_actions'])
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

    def _decode_action(self, order_dict):
        return self._decoder_actions(order_dict['actions'])
        

        

