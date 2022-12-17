from abc import ABCMeta, abstractproperty

class CreatePublication:
    
    def __call__(self, builder_publication, data):
        return builder_publication.build(self, data)

class Publication(CreatePublication, metaclass=ABCMeta):
    
    @abstractproperty
    def url(self):
        pass
    
    
class PublicationSequence(CreatePublication, metaclass=ABCMeta):
    
    @abstractproperty
    def caption(self):
        pass
    
    @abstractproperty
    def children(self):
        pass
    
class PublicationInPublicationSequence(Publication):
    
    def __init__(self, url: str, product_tags: list = []):
        self.url = url 
        self.product_pags = product_tags
        self.is_carousel_item = True
    
class SinglePublication(Publication):
    
    def __init__(self, url: str, caption: str, location_id: str = ''):
        self.url = url 
        self.caption = caption
        self.location_id = location_id
        self.is_carousel_item = False
        
    

    



        

    


