from src.model_environment.rewards.dynamic.f_class import ImportRewards


class DynamicRewards(ImportRewards):

    def from_many_modules(self, module_obj_dict):
        return {name_module : self._import_many_objects(name_module, objects_dict)
                for name_module, objects_dict in module_obj_dict.items()}

    def from_module(self, module, dict_objects):
        return self._import_many_objects(module, dict_objects)

    def one_object(self, module, name_obj, params):
        return self.import_f_class_from_module(module, name_obj)(**params)

    def one_object_dict(self, module, name_obj, params):
        return {name_obj : self.one_object(module, name_obj, params)}

    def _import_many_objects(self, module, dict_objects):
        module = self._import_module(module)
        return {name_obj : getattr(module, name_obj)(**params) 
                for name_obj, params in dict_objects.items()}
            