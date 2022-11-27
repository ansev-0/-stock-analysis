class NewsDistributor:
    def __call__(self, json_response):
        return list(map(lambda dict_: dict_[list(dict_)[1]]['tickers'], json_response))
