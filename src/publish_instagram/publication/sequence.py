from src.publish_instagram.publication.publication import PublicationSequence

class Sequence(PublicationSequence):
    
    def __init__(self, 
                 caption: str,
                 children: list,
                 location_id: str = ''):
        
        self.caption = caption
        self.children = children
        self.location_id = location_id
        self.media_type = 'CAROUSEL'
