class RewardTask:

    def __call__(self, params_dict, id_cache):
        #get copy
        params_dict = params_dict.copy()

        not_depend_on_inventory_dict = self._get_not_depend_dict(params_dict)
        if not_depend_on_inventory_dict:
            params_dict['dict_rewards']['not_depend_on_inventory'] = \
                self._update_not_depend_inventory_dict(not_depend_on_inventory_dict, id_cache)
        return params_dict

    @staticmethod
    def _get_not_depend_dict(params_dict):
        try:
            return params_dict['dict_rewards']['not_depend_on_inventory']
        except KeyError:
            return False


    def _update_not_depend_inventory_dict(self, not_depend_on_inventory_dict, id_cache):
        for module, objects in not_depend_on_inventory_dict.items():
            if module != 'rewardnode':
                self._modify_rewards(objects, id_cache)
        return not_depend_on_inventory_dict

    @staticmethod
    def _modify_rewards(objects, id_cache):
        for name_object, params_obj in objects.items():
                objects[name_object] = dict(params_obj, **{'id_cache' : id_cache})
        return objects