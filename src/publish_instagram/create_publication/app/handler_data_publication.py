class HandlerCreatePublicationApp:
    
    def __init__(self, infraestructure_connector):
        self._infraestructure_connector = infraestructure_connector
        
    def get_cursor(self, query):
        return self._infraestructure_connector.get(query)
            
            
        