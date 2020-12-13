class NameModel:

    def __init__(self, company, series, layers, train_type):
        
        self._name=None
        self._company = str(company)
        self._series = str(series)
        self._layers = str(layers)
        self._train_type = str(train_type)

        self._update_name()
        
        
    def __str__(self):
        return self.name


    def __call__(self):
        return self.name
    

    @property 
    def name(self):
        return self._name

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, company):
        self._company = str(company)
        self._update_name()


    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers):
        self._layers = str(layers)
        self._update_name()


    @property
    def series(self):
        return self._series

    @series.setter
    def series(self, series):
        self._series = str(series)
        self._update_name()


    @property
    def train_type(self):
        return self._train_type

    @train_type.setter
    def train_type(self, train_type):
        self._train_type = str(train_type)
        self._update_name()
        
        
        
    def _update_name(self):
        self_dict = dict(filter(lambda d: d[0] != '_name', self.__dict__.items()))
        self._name = '|'.join(self_dict.values())
        