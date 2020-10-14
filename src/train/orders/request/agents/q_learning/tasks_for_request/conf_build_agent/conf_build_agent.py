from src.train.orders.request.agents.q_learning.tasks_for_request.conf_build_agent.interface_epoch import InterfaceEpochTask

class ConfBuildAgentTask:
    
    _make_interface_task = InterfaceEpochTask()

    def __init__(self, train_id, stock_name, cache_id_train, cache_id_validation=None):

        self._train_id = train_id
        self._stock_name = stock_name
        self._id_cache_train = cache_id_train
        self._id_cache_validation = cache_id_validation

    def __call__(self, dict_conf):
        return {key : self._apply_sub_task(key, value)
                for key, value in dict_conf.items()}

    def _apply_sub_task(self, key, value):
        return value if 'interface_epoch' not in key \
            else self._conf_interface(value, 'validation' in key)

    
    def _conf_interface(self, dict_interface, val_data):
        return self._make_interface_task(train_id,
                                         self._stock_name,
                                         self._id_cache_validation if val_data \
                                             else self._id_cache_train,
                                         dict_interface)

