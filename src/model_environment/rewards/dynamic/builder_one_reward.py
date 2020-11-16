from src.model_environment.rewards.dynamic.f_class import ImportRewards
from src.model_environment.rewards.dynamic.build_node import BuildNode

class DynamicRewards(ImportRewards, BuildNode):

    def __init__(self, type_reward, builder_with_components=None):
        super().__init__(type_reward)
        self._builder_with_components = builder_with_components

    def from_many_modules(self, module_obj_dict):
        return {name_module : self._import_many_objects(name_module, objects_dict)
                for name_module, objects_dict in module_obj_dict.items()}

    def from_module(self, module, dict_objects):
        return self._import_many_objects(module, dict_objects)

    def one_object(self, module, name_obj, params):
        return self._build_object(self.import_f_class_from_module(module, name_obj), params)

    def one_object_dict(self, module, name_obj, params):
        return {name_obj : self.one_object(module, name_obj, params)}

    def _import_many_objects(self, module, dict_objects):
        module = self._import_module(module)
        return {name_obj : self._build_object(getattr(module, name_obj), params) 
                for name_obj, params in dict_objects.items()}

    def _build_object(self, class_object, params):
        return self._build_object_with_components(class_object, params) \
            if self._builder_with_components is not None \
            else class_object(**self.decode_node_params(**params))

    def _build_object_with_components(self, class_object, params):
        return self._builder_with_components(class_object, self.decode_node_params(**params))
        



            