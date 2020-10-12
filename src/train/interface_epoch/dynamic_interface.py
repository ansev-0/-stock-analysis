from src.tools.importer import importer

class ImportInterfaces:

    base_package = 'src.train.interface_epoch.interfaces'

    def import_interface_from_module(self, module, interface):
        return getattr(self._import_module(module), interface)

    def _import_module(self, module):
        return importer(self._join_module(module))

class DynamicInterface(ImportInterfaces):

    def interface(self, name_module, name_interface, parameters):
        return self.import_interface_from_module(name_module, name_interface)(**parameters)


    def from_dict(self, module_objects_dict):
        return {name_module : self._build_objects_from_module(name_module, objects)
                for name_module, objects in module_objects_dict.items()}

    def flatten_interfaces(self, module_objects_dict):

        return [self._build_flatten_objects_from_module(name_module, objects)
                for name_module, objects in module_objects_dict.items()]

    def _build_objects_from_module(self, name_module, objects):
        module = self._import_module(module)
        return {name_object : getattr(module, name_object)(**parameters)
                for name_object, parameters in objects.items()}

    def _build_flatten_objects_from_module(self, name_module, objects):
        module = self._import_module(module)
        return [getattr(module, name_object)(**parameters)
                for name_object, parameters in objects.items()]
