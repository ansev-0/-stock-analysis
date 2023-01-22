from src.publish_instagram.need_publish.app.publish import PublishApp
from src.publish_instagram.need_publish.infraestructure.publish_mongodb_local_connector import MongoDBLocalConnector
from src.read_database.stock_data import StockDataFromDataBase
from src.publish_instagram.need_publish.domain.filter_data import filter_significative_changes
from src.publish_instagram.need_publish.domain.need_publish import NeedPublish
from datetime import timedelta


def run_local_need_publish(names):
    connector_new_data = StockDataFromDataBase.dailyadj_dataframe()
    connector_published = PublishApp(MongoDBLocalConnector())
    filter_data = filter_significative_changes
    time_threshold = timedelta(days=1)
    need_publish = NeedPublish(connector_published,
                               connector_new_data,
                               filter_data,
                               time_threshold)
    for name in names:
        print(name)
        need_publish(name, timedelta(days=10), threshold=0.07)
        