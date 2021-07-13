from src.acquisition.acquisition.tiingo.evaluate_response.evaluate_json_response import EvaluateJsonResponse

class EvaluateJsonResponseNews(EvaluateJsonResponse):

    field_type_dict_response = {'id' : int, 
                                'title' : str,
                                'url' : str, 
                                'description' :str,
                                'publishedDate' : str, 
                                'crawlDate' : str,
                                'source' : str,
                                'tickers' : str,
                                'tags' : str}
                                