from src.publish_instagram.create_publication.domain.create_publication import CreatePublication
from src.publish_instagram.create_publication.app.build_image_file import BuildImageFile
from src.publish_instagram.create_publication.app.build_image_publication import BuildImage
from src.publish_instagram.create_publication.app.handler_data_publication import HandlerCreatePublicationApp
from src.publish_instagram.create_publication.infraestructure.get_need_publish_mongodb_local import GetAllNeedPublishMongoDBLocal
from src.publish_instagram.create_publication.infraestructure.http_saver_image import SaverImageHttp
from src.publish_instagram.create_publication.infraestructure.image_infraestructure import ImageInfraestructure
from src.publish_instagram.create_publication.infraestructure.save_publication_mongodb_local import SavePublicationMongoDBLocal
from src.publish_instagram.publication.image import Image
from src.publish_instagram.publish.domain.publish import PublishOnInstagram
from src.publish_instagram.publish.app.publish import AppPublish
from src.publish_instagram.publish.app.concrete_publish.image import PublishImageApiGraph
import json
from time import sleep
def run_local_create_publication(user_id, access_token, query):
    with open("filestore/credentials/imagebb/token.json") as f:
        token_image_bb = json.load(f)['token']
        
    #query = {'status': 'added_description'}
    builder_publication = BuildImage(build_image=BuildImageFile(ImageInfraestructure(path_icons='filestore/icons_instagram_companies',
                                                                                     path_local_images='filestore/images_instagram')),
                                     http_saver_infraestructure=SaverImageHttp(token_image_bb), 
                                     infraestructure_save_publication=SavePublicationMongoDBLocal())
    create_publication = CreatePublication(class_publication=Image, 
                                           builder_publication=builder_publication,  
                                           handler_data_publication_app=HandlerCreatePublicationApp(GetAllNeedPublishMongoDBLocal()))
    app_publish = AppPublish()
    app_publish.register_publish_types_obj(PublishImageApiGraph(user_id=user_id, access_token=access_token))
    publish = PublishOnInstagram(app_publish)
    for pub in create_publication(query):
        print('new_publication')
        print(pub.url, pub.caption)
        print('plublishing...')
        publish(pub)
        sleep(120)
