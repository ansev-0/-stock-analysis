class AddDescriptionIA:
    
    def __init__(self, model_object, connector_need_publish):
        self.model_object = model_object
        self.connector_need_publish = connector_need_publish
        
    def describe(self, data):
        description = self.model_object.predict(data)
        if description != '':
            self.connector_need_publish.publish_description(description, data)


        