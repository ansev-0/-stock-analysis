class PathModel:

    path = '/home/antonio/computer0/antonio/financialworks_models/'
    ext = '.h5'

    def __call__(self, name_model):
        self.name_model = name_model
        return self.path + name_model + self.ext



