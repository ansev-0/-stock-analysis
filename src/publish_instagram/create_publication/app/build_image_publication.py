class BuildImage:
    
    def __init__(self, http_saver_infraestructure, build_image, infraestructure_save_publication):
        self._http_saver_infraestructure = http_saver_infraestructure
        self._build_image = build_image
        self._infraestructure_save_publication = infraestructure_save_publication
        
    def build(self, image,  data: dict):
        assert 'data_image' in data
        assert 'caption' in data
        path_local_image = self._build_image(data['data_image'])
        url = self._http_saver_infraestructure(path_local_image)
        publication = image(url=url, caption=data['caption'])
        self._infraestructure_save_publication.save(publication, path_local_image, data)
        return publication
        