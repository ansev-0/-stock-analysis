class HandlerNeedDescription:
    
    def __init__(self, infraestructure_connector):
        self._infraestructure_connector = infraestructure_connector
        
    def get_cursor(self):
        for response in self._infraestructure_connector.get():
            yield response
            
        