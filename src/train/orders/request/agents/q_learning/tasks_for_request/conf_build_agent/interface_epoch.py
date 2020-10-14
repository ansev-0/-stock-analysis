
class InterfaceEpochTask:

    def __call__(self, train_id, stock_name, id_cache, interface_request):
        
        return {module : self._objects_with_new_parameters(objects, 
                                                           train_id=train_id,
                                                           id_cache=id_cache,
                                                           stock_name=stock_name) 
                for module, objects in interface_request.items()}

    def _objects_with_new_parameters(self, objects, **kwargs):
        return {name_object : dict(object_params, **kwargs)
                for name_object, object_params in objects.items()}
