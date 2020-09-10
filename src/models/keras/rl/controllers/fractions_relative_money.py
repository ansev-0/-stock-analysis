from src.models.keras.rl.controllers.abstract_controller import ControllerTransitions
from src.fit.rewards.env_rewards import make_rewards
from collections import defaultdict
from src.fit.rewards.inventory_rewards import inventory_rewards
import numpy as np


class TransitionsFractions(ControllerTransitions):



    def __init__(self, 
                 positions, 
                 init_money,
                 actions=None,
                 commision=0.5,
                 gamma_future=1, 
                 gamma_inventory=1,
                 gamma_size_transaction=0.97,
                 **kwargs):

        self._posible_func_actions = {'Buy' : self._buy_transition,
                                      'Buy_25perc' : self._buy_perc_25_transition,
                                      'Buy_50perc' : self._buy_perc_50_transition,
                                      'Buy_75perc' : self._buy_perc_75_transition,
                                      'Buy_all' : self._buy_all_transition,
                                      'Sell' : self._sell_transition, 
                                      'Sell_25perc' : self._sell_perc_25_transition,
                                      'Sell_50perc' : self._sell_perc_50_transition,
                                      'Sell_75perc' : self._sell_perc_75_transition,
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
        self._gamma_size_transaction = 0.97


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


    def eval_with_rewards(self, action, done, index, *args, **kwargs):
        return self._eval(True, action, done, index, *args, **kwargs)

    def eval_without_rewards(self, action, done, index, *args, **kwargs):
        return self._eval(False, action, done, index, *args, **kwargs)


    def _eval(self, return_future_parameters, action, done, index, *args, **kwargs):

        if done:
            # sold all at the end
            out = self._transition_done(return_future_parameters, index, *args, **kwargs)

            if out[-1]:
                self._indexes_actions['Sell_all'].append(index)
            else:
                self._indexes_actions['Predict_Sell_all'].append(index)

            return out[:-1]

        action = self._actions[action]

        for posible_action, action_func in self._posible_func_actions.items():

            if action == posible_action:
                out = action_func(return_future_parameters, index, *args, **kwargs)

                if out[-1]:
                    self._indexes_actions[action].append(index)
                else:
                    self._indexes_actions[f'Predict_{action}'].append(index)

                return out[:-1]
        # if action not in self._actions.keys()       
        self._raise_invalid_action()


    def _transition_done(self, return_future_parameters, index, inventory):

        len_inventory, value_inventory, _, inventory_not_empty = self.features_inventory(inventory)
        _, income = self._sell_many_incomes(index, len_inventory)
         
        self._money += income
        inventory = []

        if return_future_parameters:
            return self._update_reward_size_transaction(income - value_inventory, len(inventory)), \
                self._money, income, inventory, inventory_not_empty

        return self._money, income, inventory, inventory_not_empty


    def _sell_transition(self, return_future_parameters, index, inventory):
        
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)


        if inventory_not_empty:

            # remove one action of inventory
            first_value_action = inventory.pop(0) #remove one action from inventory
            inventory = self._correct_value_inventory(inventory, first_value_action - mean_inventory)

            # make balance
            gross_income, income = self._sell_incomes(index)
            self._money += income
            
            if return_future_parameters:
            # commision reward for sell is already taking in future reward
            # if mean of inventory isn't greater than current value, incr reward
                reward = self._sell_pred_rewards[index]  * self._gamma_future + \
                    inventory_rewards(mean_inventory, gross_income, 'sell') * self._gamma_inventory

                
                
                return reward, self._max_buy_next(index), income, inventory, inventory_not_empty

            return self._money, income, inventory, inventory_not_empty

        elif return_future_parameters:
            reward = self._sell_pred_rewards[index]  * self._gamma_future
            return reward, self._max_buy_next(index), 0, inventory, inventory_not_empty

        return self._money, 0, inventory, inventory_not_empty

    def _sell_perc_25_transition(self, return_future_parameters, index, inventory):
        return self._sell_perc_transition(return_future_parameters, index, inventory, 0.25)

    def _sell_perc_50_transition(self, return_future_parameters, index, inventory):
        return self._sell_perc_transition(return_future_parameters, index, inventory, 0.50)

    def _sell_perc_75_transition(self, return_future_parameters, index, inventory):
        return self._sell_perc_transition(return_future_parameters, index, inventory, 0.75)


    def _sell_perc_transition(self, return_future_parameters, index, inventory, perc):

        len_inventory, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)

        
        if inventory_not_empty:
            #calculate size transaction
            n =  self._calculate_size_sell_transaction(perc, len_inventory)

            #update len and value inventory
            stock_remove = inventory[:n]
            inventory = inventory[n:]

            inventory = self._correct_value_inventory(inventory, sum(stock_remove) - mean_inventory * n)
            #calculate balance and update money
            unit_gross_income, _, _, income = self._sell_many_incomes(index, n, return_unit=True)
            self._money += income
            
            if return_future_parameters:
                #calculate reward
                reward = (inventory_rewards(mean_inventory, unit_gross_income, 'sell')  * self._gamma_inventory + 
                          self._sell_pred_rewards[index] * self._gamma_future) * n 



                return self._update_reward_size_transaction(reward, n), self._max_buy_next(index), \
                     income, inventory, inventory_not_empty

            return self._money, income, inventory, inventory_not_empty

        elif return_future_parameters:
            reward = self._sell_pred_rewards[index] * self._gamma_future

            return reward, self._max_buy_next(index), 0, inventory, inventory_not_empty
            
        return self._money, 0, inventory, inventory_not_empty



    def _sell_all_transition(self, return_future_parameters, index, inventory):
        
        len_inventory, value_inventory, _, inventory_not_empty = self.features_inventory(inventory)


        if inventory_not_empty:
            # remove inventory
            inventory = []
            # calculate income and update money
            gross_income, income = self._sell_many_incomes(index, len_inventory)
            self._money += income
            # commision for sell is already taking in future reward
            if return_future_parameters:
                # reward
                reward = (inventory_rewards(value_inventory, gross_income, 'sell') * self._gamma_inventory \
                    + len_inventory * self._sell_pred_rewards[index] * self._gamma_future) 
                        


                return self._update_reward_size_transaction(reward, len_inventory), \
                    self._max_buy_next(index), income, inventory, inventory_not_empty

            return self._money, income, inventory, inventory_not_empty

        elif return_future_parameters:

            reward = self._sell_pred_rewards[index] * self._gamma_future
            return reward, self._max_buy_next(index), 0, inventory, inventory_not_empty

        return self._money, 0, inventory, inventory_not_empty

    def _buy_transition(self, return_future_parameters, index, inventory):

        # features of inventory
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)
        current_value = self._positions[index]
        enough_money = current_value + self._commision <= self._money


        if enough_money:
            inventory.append(current_value) # add to inventory
            _, income = self._buy_incomes(index)
            self._money += income # update money

            if return_future_parameters:
                # reward inventory
                # if mean of inventory is greater than current value incr reward
                reward_inventory = inventory_rewards(mean_inventory, 
                                                     current_value,
                                                     'buy') * self._gamma_inventory if inventory_not_empty else 0
             # total reward
                reward = self._buy_pred_rewards[index] * self._gamma_future + reward_inventory
                return reward, self._max_buy_next(index), income, inventory, enough_money

            return self._money, income, inventory, enough_money

        elif return_future_parameters:
            reward = self._buy_pred_rewards[index] * self._gamma_future
            return reward, self._max_buy_next(index), 0, inventory, enough_money

        return self._money, 0, inventory, enough_money




    def _buy_perc_25_transition(self, return_future_parameters, index, inventory):
        return self._buy_perc_transition(return_future_parameters, index, inventory, 0.25)

    def _buy_perc_50_transition(self, return_future_parameters, index, inventory):
        return self._buy_perc_transition(return_future_parameters, index, inventory, 0.5)

    def _buy_perc_75_transition(self, return_future_parameters, index, inventory):
        return self._buy_perc_transition(return_future_parameters, index, inventory, 0.75)

    def _buy_perc_transition(self,return_future_parameters, index, inventory, perc):

        # features of inventory
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)
        # get current position
        current_value = self._positions[index]
        # check if enough money
        enough_money = current_value + self._commision <= self._money

        if enough_money:
            # get size of transaction
            n = self._calculate_size_buy_transaction(perc, current_value)
            # add to inventory
            inventory.extend([current_value] * n) 
            #calculate balance and update money
            _, income = self._buy_many_incomes(index, n)
            self._money += income 

            if return_future_parameters:
                # reward inventory
                # if mean of inventory is greater than current value incr reward
                reward_inventory = inventory_rewards(mean_inventory, 
                                                     current_value,
                                                     'buy') * self._gamma_inventory  if inventory_not_empty else 0
                 # total reward
                reward = (self._buy_pred_rewards[index] * self._gamma_future  + reward_inventory) * n 
                return self._update_reward_size_transaction(reward, n),\
                     self._max_buy_next(index), income, inventory, enough_money

            return self._money, income, inventory, enough_money
            
        elif return_future_parameters:
            reward = self._buy_pred_rewards[index] * self._gamma_future 
            return reward, self._max_buy_next(index), 0, inventory, enough_money

        return self._money, 0, inventory, enough_money


    def _buy_all_transition(self, return_future_parameters, index, inventory):

        # features of inventory
        _, _, mean_inventory, inventory_not_empty = self.features_inventory(inventory)
        current_value = self._positions[index]
        enough_money = current_value + self._commision  <= self._money

        if enough_money:

            n = self._money // (current_value + self._commision)# n to buy
            inventory.extend([current_value] * int(n)) # add to inventory
            _, income = self._buy_many_incomes(index, n)
            self._money += income # update money
            # reward inventory
            # if mean of inventory is greater than current value incr reward
            if return_future_parameters:

                reward_inventory = inventory_rewards(mean_inventory,
                                                    current_value, 'buy') * n * self._gamma_inventory \
                    if inventory_not_empty else 0
                
                # total reward
                reward = (self._buy_pred_rewards[index] * self._gamma_future  + reward_inventory) * n
                return self._update_reward_size_transaction(reward, n),\
                     self._max_buy_next(index), income, inventory, enough_money

            return self._money, income, inventory, enough_money

        elif return_future_parameters:
            
            reward = self._buy_pred_rewards[index] * self._gamma_future
            return reward, self._max_buy_next(index), 0, inventory, enough_money

        return self._money, 0, inventory, enough_money

    def _not_actions_transition(self, return_future_parameters, index, inventory):
        if return_future_parameters:
            return self._not_actions_pred_rewards[index], self._max_buy_next(index), 0, inventory, True
        return self._money, 0, inventory, True

    def _update_reward_size_transaction(self, reward, size):
        cost = np.abs(reward) * (1 - self._gamma_size_transaction ** size) 
        return reward - cost 

    @staticmethod
    def _correct_value_inventory(inventory, diff):
        new_len_inventory = len(inventory)

        if new_len_inventory > 0:
            mean_diff = diff / new_len_inventory
            return [value + mean_diff for value in inventory]
        return inventory

    def _max_buy_next(self, index):
        return self._money // self._calculate_size_buy_transaction(1, self._positions[index + 1])

    @staticmethod
    def _calculate_size_sell_transaction(perc, len_inventory):
        n = int(len_inventory * perc)
        return n if n > 0 else 1

    def _calculate_size_buy_transaction(self, perc, current_value):   
            n = int(self._money // (self._commision + current_value) * perc)
            return  n if n > 0 else 1

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

