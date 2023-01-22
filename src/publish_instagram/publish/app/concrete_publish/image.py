from instagram_client.instagram_api.adapters.request_session_adapter import RequestsGraphInstagram
from src.publish_instagram.publication.image import Image

class PublishImageApiGraph:
    _TYPE_ACCEPTED = Image
    _PARAMS = ( 
               'caption',
               'location_id',
               'product_tags',
               'user_tags'
    )
    def __init__(self, access_token, user_id):
        self.__user_id = user_id
        self.__access_token = access_token
        self.__make_requests = RequestsGraphInstagram(self.__access_token)


    def publish(self, publication: Image):
        response = self.__make_requests.post_user_image(user_id=self.__user_id,
                                                        image_url=publication.url,
                                                        params={key : getattr(publication, key) 
                                                                for key in self._PARAMS 
                                                                if getattr(publication, key)})
        if not response.ok:
            return response
        
        response = self.__make_requests.post_media_publish(user_id=self.__user_id,
                                                           creation_id=response.json()['id'])
        if not response.ok:
            return response
        return response.json()
    
        

        
    
    
    