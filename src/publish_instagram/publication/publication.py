from abc import ABCMeta, abstractproperty

class Publication(metaclass=ABCMeta):
    
    @abstractproperty
    def url(self):
        pass
    
class PublicationSequence(metaclass=ABCMeta):
    
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
        
    
class Image(SinglePublication):
    
    def __init__(self, 
                 url: str, 
                 caption: str, 
                 location_id: str = '', 
                 product_tags: list = [],
                 user_tags: list=[]):
        
        super().__init__(url, caption, location_id)
        self.product_tags = product_tags
        self.user_tags = user_tags
    
class Video(SinglePublication):
    
    def __init__(self,
                 url: str,
                 caption: str,
                 product_tags: list = [],
                 location_id: str = '',
                 thumb_offset: int = 0):
        
        super().__init__(url, caption, location_id)
        self.product_tags = product_tags
        self.media_type = 'VIDEO'
        self.thumb_offset = thumb_offset

class Reel(SinglePublication):
    
    def __init__(self, url: str,
                 caption: str,
                 location_id: str = '',
                 share_to_feed: bool = True,
                 thumb_offset: int = 0):
        
        super().__init__(url, caption, location_id)
        self.share_to_feed = share_to_feed
        self.media_type = 'REELS'
        self.thumb_offset = thumb_offset
        
class ImageInSequence(PublicationInPublicationSequence):
    
    def __init__(self, 
                 url: str,
                 product_tags: list = [],
                 user_tags: list = []):
        
        super().__init__(url, product_tags)
        self.user_tags = user_tags
        
    
class VideoInSequence(PublicationInPublicationSequence):
    
    def __init__(self, 
                 url: str, product_tags: list = [],
                 thumb_offset: int = 0):
        super().__init__(url, product_tags)
        self.media_type = 'VIDEO'
        self.thumb_offset = thumb_offset

class Sequence(PublicationSequence):
    
    def __init__(self, 
                 caption: str,
                 children: list,
                 location_id: str = ''):
        
        self.caption = caption
        self.children = children
        self.location_id = location_id
        self.media_type = 'CAROUSEL'
