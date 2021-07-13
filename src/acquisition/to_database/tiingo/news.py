from src.acquisition.to_database.tiingo.to_database import TiingoToDB
from src.acquisition.to_database.tiingo.distributor.news_distributor import NewsDistributor
from src.acquisition.to_database.tiingo.process_response.news import ProcessResponseNews
from src.acquisition.to_database.tiingo.saver.news import SaverTiingoNews
from src.acquisition.acquisition.tiingo.evaluate_response.news import EvaluateJsonResponseNews
from src.acquisition.acquisition.tiingo.client import get_client


class TiingoToDBNews(TiingoToDB):
    client = get_client()
    saver = SaverTiingoNews()
    distributor = NewsDistributor()
    evaluate_response = EvaluateJsonResponseNews()
    process_response = ProcessResponseNews()
