from src.tools.importer import importer

class ImportRewards:
    
    base_package = 'src.model_environment.rewards'
    
    def __init__(self, type_reward):
        self._package = None
        self.type_reward = type_reward
    
    @classmethod
    def depend_on_inventory(cls):
        return cls('depend_on_inventory')
    
    @classmethod
    def not_depend_on_inventory(cls):
        return cls('not_depend_on_inventory')
    
    @classmethod
    def profit(cls):
        return cls('profit')
    
    @property
    def package(self):
        return self._package
    
    @property
    def type_reward(self):
        return self._type_reward
    
    @type_reward.setter
    def type_reward(self, type_reward):
        self._package = f'{self.base_package}.{type_reward}.rewards'
        self._type_reward = type_reward
        
        
    def __call__(self, module, objects):
    
        if isinstance(objects, str):
            return self._import_one_object(module, objects)
        
        elif isinstance(objects, tuple) or isinstance(objects, list):
            return self._import_many_objects(module, objects)
        
        raise TypeError('You must pass a instance of str or a list / tuple of instances')
        
    #private methods of instance

    def _import_one_object(self, module, objects):
        return {objects : getattr(self._import_module(module), objects)}

    def _import_many_objects(self, module, objects):
        return {obj : getattr(self._import_module(module), obj)
                for obj in objects}
    
    
    def _import_module(self, module):
        return importer(self._join_module(module))
    
    def _join_module(self, module):
        return f'{self._package}.{module}'