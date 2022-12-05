from src.publish_instagram.publication.publication import SinglePublication

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