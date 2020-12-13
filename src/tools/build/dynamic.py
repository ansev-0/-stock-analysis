class BuilderWithComponents:
    '''
    This class aims to build the commons needed by the reward objects and by the objects that simulate the environment. 
    This saves calls to the database.
    '''
    components = {}

    def register_component(self, name_component, component):
        self.components[name_component] = component
        self.components = self.components.copy()

    def __call__(self, class_object, dkwargs):
        return class_object(**dkwargs, **self._filter_valids_components(class_object))

    def _filter_valids_components(self,  class_object):
        return {name : component for name, component in self.components.items()
                if name in class_object.__init__.__code__.co_varnames}
