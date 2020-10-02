from src.model_environment.run.run import RunEnv

class RunQlearningEnv(RunEnv):

    def transition(self, action, n_stocks=None, frac=None):  
        _,_, action_done, income = self.states_actions.do_action(action, n_stocks, frac)
        self.indexes_actions.save(action, self.states_actions.time, action_done, n_stocks, frac)

        if not self.states_actions.terminal:
            self.states_actions.step()

        profit = self.states_actions.profit

        return profit, income, self.states_actions.max_purchases(),\
             self.states_actions.max_sales()

    def transition_with_rewards(self, action, n_stocks=None, frac=None):

        real_frac, real_n_stocks, action_done, income = self.states_actions.do_action(action, n_stocks, frac)
        self.indexes_actions.save(action, self.states_actions.time, action_done, n_stocks, frac)

        price = self.states_actions.stock_price
        time = self.states_actions.time
        
        if not self.states_actions.terminal:
            self.states_actions.step()

        profit = self.states_actions.profit



        if action_done:
            rewards = self.reward_action_done.reward(profit = profit, 
                                                     action=action, time=time, 
                                                     n_stocks=real_n_stocks, 
                                                     price = price,
                                                     frac=real_frac)   
        else:
            rewards = self.reward_action_not_done.reward(profit = profit, 
                                                         action=action, time=time,
                                                         price = price)



        return rewards, (profit, income, self.states_actions.max_purchases(), \
            self.states_actions.max_sales())

    @staticmethod
    def _check_valid_action(action):
        if action not in ('buy', 'sell', 'no_action'):
            raise ValueError('You must pass buy, sell or no_action')


class RunEnvAdaptQlearningModel(RunQlearningEnv):

    def __init__(self, adapter, *args, **kwargs):
        self.adapter = adapter
        self.action_spaces = list(self.adapter)
        super().__init__(*args, **kwargs)

    def eval_with_rewards(self, action):
        return self.transition_with_rewards(**self.adapter[action])

    def eval_without_rewards(self, action):
        return self.transition(**self.adapter[action])