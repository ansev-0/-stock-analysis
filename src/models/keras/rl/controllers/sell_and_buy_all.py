from src.models.keras.rl.controllers.abstract_controller import ControllerTransitions
from src.fit.rewards.env_rewards import make_rewards
from collections import defaultdict
from src.fit.rewards.inventory_rewards import inventory_rewards
import numpy as np


class TransitionsSellBuyAll(ControllerTransitions):



    def __init__(self, 
                 positions, 
                 init_money,
                 actions=None,
                 commision=0.5,
                 gamma_future=1, 
                 gamma_inventory=1,
                 **kwargs):

        self._posible_func_actions = {'Buy' : self._buy_transition,
                                      'Buy_all' : self._buy_all_transition,
                                      'Sell' : self._sell_transition, 
                                      'Sell_all' : self._sell_all_transition, 
                                      'No_actions' : self._not_actions_transition}

        self._indexes_actions = None
        self.reset_transitions()                            
        
        self.init_money = init_money
        self._money = init_money
        self._commision = commision
        self._positions = positions
        self._gamma_future = gamma_future
        self._gamma_inventory = gamma_inventory


        self._not_actions_pred_rewards, self._sell_pred_rewards, self._buy_pred_rewards = \
            make_rewards(positions, commision, **kwargs)



        if self._use_default_actions(actions):
            self._actions = self._default_actions()

        else:
            self._actions = actions
            self._check_is_dict_actions()
            self._check_valid_values_actions()


    @property
    def actions(self):
        return self._actions

    @property
    def current_money(self):
        return self._money

    def reset_money(self):
        self._money = self.init_money

    def reset_transitions(self):
        self._indexes_actions = defaultdict(list)

    @property
    def indexes_actions(self):
        return self._indexes_actions

    @property
    def counters(self):
        return {key : len(value) for key, value in self._indexes_actions.items()}
    
    @property
    def commision(self):
        return self._commision


    def eval(self, action, done, index, *args, **kwargs):

        if done:
            # sold all at the end
            self._indexes_actions['Sell_all'].append(index)
            return self._transition_done(index, *args, **kwargs)

        action = self._actions[action]

        for posible_action, action_func in self._posible_func_actions.items():

            if action == posible_action:
                out = action_func(index, *args, **kwargs)

                if out[-1]:
                    self._indexes_actions[action].append(index)
                else:
                    self._indexes_actions[f'Predict_{action}'].append(index)

                return out[:-1]
                
            

        # if action not in self._actions.keys()       
        self._raise_invalid_action()


    def _transition_done(self, index, inventory):

        _, income = self._sell_many_incomes(index, len(inventory))
        reward = income - sum(inventory)
        self._money += income
        inventory = []
        return reward, self._money, income, inventory


    def _sell_transition(self, index, inventory):
        
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)

        # future rewards
        unit_reward_future = self._sell_pred_rewards[index]
        unit_reward_future *= self._gamma_future

        if inventory_not_empty:

            gross_income, income = self._sell_incomes(index)
            self._money += income

            # based on inventory
            # commision reward for sell is already taking in future reward
            reward_inventory = inventory_rewards(mean_inventory, gross_income, 'sell') * self._gamma_inventory
            first_value_action = inventory.pop(0) #remove one action from inventory

            # if mean of inventory isn't greater than current value, incr reward
            diff_value = first_value_action - mean_inventory

            if len(inventory) > 0:
                diff_mean = diff_value / len(inventory)
                inventory = [val - diff_mean for val in inventory]

            reward = unit_reward_future + reward_inventory

        else:


            income = 0
            reward = unit_reward_future

        return reward, self._money, income, inventory, inventory_not_empty



    def _sell_all_transition(self, index, inventory):
        
        len_inventory, value_inventory, _, inventory_not_empty = self.features_inventory(inventory)
        
        unit_reward_future = self._sell_pred_rewards[index] * self._gamma_future


        if inventory_not_empty:
            

            # future
            total_reward_future = len_inventory * unit_reward_future
            # based on inventory
            gross_income, income = self._sell_many_incomes(index, len_inventory)
            self._money += income

                # commision for sell is already taking in future reward
            reward_inventory = inventory_rewards(value_inventory, gross_income, 'sell') * self._gamma_inventory
            reward = reward_inventory + total_reward_future

            # remove inventory
            inventory = []
            
        else:
            
            reward = unit_reward_future
            income = 0


        return reward, self._money, income, inventory, inventory_not_empty
        

    def _buy_transition(self, index, inventory):

        # features of inventory
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)
        current_value = self._positions[index]



        enough_money = current_value <= self._money
        unit_reward_future = self._buy_pred_rewards[index] * self._gamma_future


        if enough_money:

            inventory.append(current_value) # add to inventory
            _, income = self._buy_incomes(index)
            self._money += income # update money

            # reward inventory
            # if mean of inventory is greater than current value incr reward
            reward_inventory = inventory_rewards(mean_inventory, 
                                                 current_value,
                                                 'buy') * self._gamma_inventory if inventory_not_empty else 0


             # total reward
            reward = unit_reward_future + reward_inventory

        else:

            reward = unit_reward_future
            income = 0

        return reward, self._money, income, inventory, enough_money


    def _buy_all_transition(self, index, inventory):

        # features of inventory
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)
        current_value = self._positions[index]
        # reward future
        unit_reward_future = self._buy_pred_rewards[index] * self._gamma_future

        enough_money = current_value  <= self._money

        if enough_money:

            
            n = self._money // current_value # n to buy
            inventory.extend([current_value] * int(n)) # add to inventory
            _, income = self._buy_many_incomes(index, n)
            self._money += income # update money

            # reward inventory
            # if mean of inventory is greater than current value incr reward
            reward_inventory = inventory_rewards(mean_inventory,
                                                current_value, 'buy') * n * self._gamma_inventory \
                if inventory_not_empty else 0
                
             # total reward
            total_reward_future = unit_reward_future * n
            reward = total_reward_future + reward_inventory

        else:
            
            reward = unit_reward_future
            income = 0

        return reward, self._money, income, inventory, enough_money


    def _buy_incomes(self, index):
        gross_income = -self._positions[index]
        income = gross_income - self._commision
        return gross_income, income

    def _buy_many_incomes(self, index, n, return_unit=False):
        unit_gross_income, unit_income = self._buy_incomes(index)
        gross_income = unit_gross_income * n
        income = unit_income * n

        if return_unit:
            return unit_gross_income, unit_income, gross_income, income
        return gross_income, income

    def _sell_incomes(self, index):
        gross_income = self._positions[index]
        income = gross_income - self._commision
        return gross_income, income

    def _sell_many_incomes(self, index, n, return_unit=False):
        unit_gross_income, unit_income = self._sell_incomes(index)
        gross_income = unit_gross_income * n
        income = unit_income * n

        if return_unit:
            return unit_gross_income, unit_income, gross_income, income
        return gross_income, income



    def _not_actions_transition(self, index, inventory):
        unit_reward_future = self._not_actions_pred_rewards[index]
        reward = unit_reward_future
        return reward, self._money, 0, inventory, True


    def _raise_invalid_action(self):
        valid_actions_values = ' or '.join(self._actions.keys())
        raise ValueError(f'Invalid action, You must pass : {valid_actions_values}')


    @staticmethod
    def features_inventory(inventory):

        len_inventory = len(inventory)
        value_inventory = sum(inventory)
        inventory_not_empty = len_inventory > 0
    
        mean = value_inventory / len_inventory if inventory_not_empty else np.nan
   
        return len_inventory, value_inventory, mean, inventory_not_empty 

    def _use_default_actions(self, actions):
        return actions is None
            

    def _default_actions(self):
        return dict(enumerate(self._posible_func_actions.keys()))

    def _check_is_dict_actions(self):
        if not isinstance(self._actions, dict):
            raise ValueError('You must pass a dict')

    def _check_valid_values_actions(self):
        if sorted(tuple(self._actions.values())) != tuple(self._posible_func_actions.keys()):
            raise ValueError('Values are incorrect')

