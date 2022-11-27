
class AcquisitionJob:

    def __init__(self, task_obj, apply):
        self.task_obj = task_obj
        self.apply = apply
        self._check_run_is_available()
        self._run = getattr(self.task_obj, self.apply['method'])

    def __call__(self):
        return self._run(*self.apply['args'], **self.apply['kwargs'])

    def _check_run_is_available(self):
        if not hasattr(self.task_obj, self.apply['method']):
            raise AttributeError('task_obj has not method {}'.format(self.apply['method']))