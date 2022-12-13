class AdminQueryOpenAi:
    
    def __call__(self, response):
        try:
            return response.choices[0]['text']
        except Exception as error:
            print(error)
            return ''