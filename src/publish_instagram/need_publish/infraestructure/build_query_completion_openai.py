class BuildQueryCompletionOpenAI:
    
    DEFAULT_PARAMETERS = {"model": "text-davinci-003",
                          "max_tokens": 300}
    
    def __init__(self, build_prompt_with_data):
        self._build_prompt_with_data = build_prompt_with_data
        
    def __call__(self, data, **kwargs):
        parameters = dict(self.DEFAULT_PARAMETERS, **kwargs)
        return dict(parameters, **{'prompt': self._build_prompt_with_data(data, **kwargs)})