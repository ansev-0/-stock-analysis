class AddDescription:
    
    def __init__(self, add_description_app, handler_need_description_app):
        self._add_description_app = add_description_app
        self._handler_need_description_app = handler_need_description_app 
        
    def __call__(self, **kwargs):
        for data in self._handler_need_description_app.get_cursor():
            self._add_description_app.describe(data, **kwargs)
