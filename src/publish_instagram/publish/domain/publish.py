from src.publish_instagram.publication.publication import Publication, PublicationSequence
from typing import Union

class PublishOnInstagram:
    
    def __init__(self, app_connector):
        self._app_connector = app_connector
        
    def __call__(self, publication: Union[Publication, PublicationSequence]):
        return self._app_connector.publish(publication)
