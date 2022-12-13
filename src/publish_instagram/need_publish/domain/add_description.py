class AddDescription:
    
    def __init__(self, add_description_app):
        self._add_description_app = add_description_app
        
    def __call__(self, data, **kwargs):
        return self._add_description_app.describe(data, **kwargs)
