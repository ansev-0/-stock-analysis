from src.publish_instagram.publication.publication import SinglePublication, PublicationInPublicationSequence

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
        
class ImageInSequence(PublicationInPublicationSequence):
    
    def __init__(self, 
                 url: str,
                 product_tags: list = [],
                 user_tags: list = []):
        
        super().__init__(url, product_tags)
        self.user_tags = user_tags