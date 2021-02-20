
class Asset:

    def __init__(self, name, 
                       label, 
                       enemy_assets=None, 
                       stakeholders=None, 
                       products=None, 
                       relate_words=None):

        self._name = name
        self._label = label
        self._products = products
        self._stakeholders = stakeholders
        self._enemy_assets = enemy_assets
        self._relate_words = relate_words

    @property
    def key_words(self):
        return {(key[1:] if key.startswith('_') else key) : value 
                for key, value in self.__dict__.items()}

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def products(self):
        return self._products

    def add_products(self, products):
        self._products = self._set_new_value(self._products, products)

    @property
    def stakeholders(self):
        return self._stakeholders
    
    def add_stakeholders(self, stakeholders):
        self._stakeholders = self._set_new_value(self._stakeholders, stakeholders)

    @property
    def enemy_assets(self):
        return self._enemy_assets

    
    def add_enemy_assets(self, enemy_assets):
        self._enemy_assets = self._set_new_value(self._enemy_assets, enemy_assets)

    @property
    def relate_words(self):
        return self._relate_words

    def add_relate_words(self, relate_words):
        self._relate_words = self._set_new_value(self._relate_words, relate_words)


    def _set_new_value(self, where, value):
        value = value if isinstance(value, list) else [value]
        where = where + value if where is not None else value
        
