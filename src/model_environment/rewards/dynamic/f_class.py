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
           
    def import_f_class_from_module(self, module, f_class):
        return getattr(self._import_module(module), f_class)
    
    def _import_module(self, module):
        return importer(self._join_module(module))
    
    def _join_module(self, module):
        return f'{self._package}.{module}'

        

class ImportDictRewards(ImportRewards):

    def from_many_modules(self, module_f_class_dict):
        return {name_module : self._import_from_module(name_module, f_classes)
                for name_module, f_classes in module_f_class_dict.items()}

    def from_module(self, module, f_classes):
        return self._import_from_module(module, f_classes)

    def one_f_class_from_module(self, module, f_class):
        return self._import_one_f_class(module, f_class)

    #private methods of instance
    def _import_from_module(self, module, f_classes):
        if isinstance(f_classes, str):
            return self._import_one_f_class(module, f_classes)
        
        elif isinstance(f_classes, tuple) or isinstance(f_classes, list):
            return self._import_many_f_class(module, f_classes)
        raise TypeError('''You must pass a instance of str
                         or a list / tuple of instances''')

    def _import_many_f_class(self, module, f_classes):
        module = self._import_module(module)
        return {f_class : getattr(module, f_class) 
                for f_class in f_classes}

    def _import_one_f_class(self, module, f_class):
        return {f_class : self.import_f_class_from_module(module, f_class)}
        