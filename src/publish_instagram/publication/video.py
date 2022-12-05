from src.publish_instagram.publication.publication import SinglePublication, PublicationInPublicationSequence

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

class VideoInSequence(PublicationInPublicationSequence):
    
    def __init__(self, 
                 url: str, product_tags: list = [],
                 thumb_offset: int = 0):
        super().__init__(url, product_tags)
        self.media_type = 'VIDEO'
        self.thumb_offset = thumb_offset
               