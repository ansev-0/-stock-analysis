from src.publish_instagram.publication.publication import Publication, PublicationSequence
from typing import Union

class AppPublish:

    def publish(self, publication: Union[Publication, PublicationSequence]):
        assert isinstance(publication, (Publication, PublicationSequence))
        return self._get_publish_obj(publication).publish(publication)
        
        
    def _get_publish_obj(self, publication):
        for obj in self.__dict__.values():
            if hasattr(obj, '_TYPE_ACCEPTED') and (obj._TYPE_ACCEPTED == type(publication)):
                return obj
            
    def register_publish_types_obj(self, publish_type_obj):
        assert hasattr(publish_type_obj, '_TYPE_ACCEPTED')
        setattr(self, publish_type_obj.__class__.__name__.lower(), publish_type_obj)
        
        