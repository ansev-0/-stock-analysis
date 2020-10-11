
class InterfaceEpochTask:

    def __call__(self, id_cache, interface_request):
        
        return {module : self._objects_with_id_cache_parameter_updates(objects, id_cache) 
                for module, objects in interface_request.items()}

    def _objects_with_id_cache_parameter_updates(self, objects, id_cache):
        return {name_object : dict(object_params, **{'id_cache' : id_cache})
                for name_object, object_params in objects.items()}
            




