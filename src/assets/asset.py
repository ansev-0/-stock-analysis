
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

import numpy as np        
assets = (
    {
     'name' : 'Apple',
     'label' : 'AAPL',
     'enemy_assets' : np.nan,
     'stakeholders' : np.nan,
     'products' : ('iphone', 'apple watch', 'iPad', 'iPod', 'Mac', 'iCloud', 'HomePod', 'AirPlay', 'Apple TV'),
     'relate_words' : np.nan,

     },

    {
     'name' : 'Google',
     'label' : 'GOOGL',
     'enemy_assets' : np.nan,
     'stakeholders' : np.nan,
     'products' : ('google drive', 'gmail', 'google photos', 'google news', 'google chrome', 'google chromecast', 'google store', ),
     'relate_words' : np.nan

     },

    {
     'name' : 'Twitter',
     'label' : 'TWTR',
     'enemy_assets' : np.nan,
     'stakeholders' : np.nan,
     'products' : np.nan,
     'relate_words' : np.nan

     },


    {
     'name' : 'Nvidia',
     'label' : 'NVDA',
     'enemy_assets' : ('AMD',),
     'stakeholders' : np.nan,
     'products' : ('nvidia gpu', 'nvidia geforce', 'nvidia titan', 
                   'nvidia quadro', 'nvidia jetson', 
                   'nvidia gpu cloud', 'nvidia shield', ),
     'relate_words' : np.nan

     },

    {
     'name' : 'AMD',
     'label' : 'AMD',
     'enemy_assets' : ('NVDA'),
     'stakeholders' : np.nan,
     'products' : ('amd rayzen', 'amd gpu', 'amd radeon', 'amd epyc', 'amd instinct', 'amd cpu', ),
     'relate_words' : np.nan

     },

    {
     'name' : 'Amazon',
     'label' : 'AMZN',
     'enemy_assets' : np.nan,
     'stakeholders' : np.nan,
     'products' : ('aws', 'amazon prime', 'amazon music', 'amazon photos', ),
     'relate_words' : np.nan

     },

    {
     'name' : 'Tesla',
     'label' : 'TSLA',
     'enemy_assets' : np.nan,
     'stakeholders' : ('Elon Musk', ),
     'products' : ('tesla car', 'tesla electric car', 'tesla solar', ),
     'relate_words' : np.nan

     },


)