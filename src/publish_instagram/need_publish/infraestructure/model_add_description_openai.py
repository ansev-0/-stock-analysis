import openai

class ModelAddDescriptionCompletionOpenAI:
    
    def __init__(self, get_password_method, build_query_completion_openai, admin_response_openai):
        self.__get_password_method = get_password_method
        self.__build_query_completion_openai = build_query_completion_openai
        self.__admin_response_openai = admin_response_openai
        
    def predict(self, data, **kwargs):
        openai.api_key = self.__get_password_method()
        return self.__admin_response_openai(
            openai.Completion.create(
            **self.__build_query_completion_openai(data, **kwargs)
            )
        )