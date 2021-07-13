class NewsDistributor:
    def __call__(self, json_response):
        return json_response['tickers']
