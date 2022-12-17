from src.publish_instagram.need_publish.domain.add_description import AddDescription
from src.publish_instagram.need_publish.app.add_description_ia import AddDescriptionIA
from src.publish_instagram.need_publish.app.handler_need_description import HandlerNeedDescription
from src.publish_instagram.need_publish.infraestructure.get_credentials_openai import GetCredentials
from src.publish_instagram.need_publish.infraestructure.build_query_completion_openai import BuildQueryCompletionOpenAI
from src.publish_instagram.need_publish.infraestructure.build_prompt_current import build_prompt_current
from src.publish_instagram.need_publish.infraestructure.model_add_description_openai import ModelAddDescriptionCompletionOpenAI
from src.publish_instagram.need_publish.infraestructure.admin_response_openai import AdminQueryOpenAi
from src.publish_instagram.need_publish.infraestructure.publish_description_local_connector import PublishDescription
from src.publish_instagram.need_publish.infraestructure.get_stocks_without_description_local_connector import StocksWithoutDescriptions


def add_description_run(config_description={}):
    get_description = ModelAddDescriptionCompletionOpenAI(admin_response_openai=AdminQueryOpenAi(),
                                                          get_password_method=GetCredentials(), 
                                                          build_query_completion_openai=BuildQueryCompletionOpenAI(build_prompt_current))
    add_description_app = AddDescriptionIA(get_description, PublishDescription())
    handler_need_description_app = HandlerNeedDescription(StocksWithoutDescriptions())

    return AddDescription(add_description_app, handler_need_description_app)(**config_description)


