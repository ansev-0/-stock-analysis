from src.model_environment.rewards.dynamic.rewards import ImportRewards

class DynamicRewards(ImportRewards):
    
    def __call__(self, module, objects, parameters):
        
        if self._one_reward(objects, parameters):
            return self._one_reward (module, objects, parameters)
        return self._many_reward(module, objects, parameters)

        
    def _many_rewards(self, module, objects, parameters):
        
        return {dict_class[0] : dict_class[1](**parameters[i])
                for i, dict_class in enumerate(super().__call__(module, objects).items())}
            
        
    def _one_reward(self, module, objects, parameters):
        return super().__call__(module, objects)(**parameters)
    
        
  
    def _one_reward(self, objects, parameters):
        
        one_object = isinstance(objects, str)
        one_dict_parameters = isinstance(parameters, dict)
        
        if (one_object and not one_dict_parameters) or \
            (not one_object and one_dict_parameters):
            raise ValueError('You must pass the same number of objects and dict parameters')
        elif isinstance(objects, list) or isinstance(objects, tuple):
            self._check_eq_len(objects, parameters)

        return one_object
            

    @staticmethod
    def _check_eq_len(objects, parameters):
        if not len(objects) == len(parameters):
            raise ValueError('Objects mut be same length than parameters')
            