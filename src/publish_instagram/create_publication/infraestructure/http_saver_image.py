from imgbbpy import SyncClient

class SaverImageHttp:
    
    def __init__(self, api_key):
        self.__apikey = api_key
        self.__client = SyncClient(self.__apikey)
        
    def __call__(self, file, expiration=60*60*24):
        image = self.__client.upload(file=file, expiration=expiration)
        return image.url
