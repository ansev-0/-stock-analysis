from src.tools.importer import importer

class DynamicCommision:
    base_package = 'src.train.rl_model.commision'

    def __call__(self, broker):
        return getattr(self._import_module(broker), f'Commision{broker.capitalize()}')

    def _join_module(self, broker):
        return f'{self.base_package}.{broker}.{broker}'

    def _import_module(self, broker):
        return importer(self._join_module(broker))

