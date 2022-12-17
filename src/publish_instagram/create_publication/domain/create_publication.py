class CreatePublication:
    
    def __init__(self, class_publication, builder_publication, handler_data_publication_app):
        self._handler_data_publication_app = handler_data_publication_app
        self._builder_publication = builder_publication
        self._class_publication = class_publication
        
    def __call__(self, handler_query):
        for data in self._handler_data_publication_app.get_cursor(handler_query):
            try:
                yield self._class_publication.from_builder(self._builder_publication, data)
            except Exception as error:
                print(error)
                yield None
