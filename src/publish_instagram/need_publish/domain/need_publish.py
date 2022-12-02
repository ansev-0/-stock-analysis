
from datetime import datetime

class NeedPublish:
    
    def __init__(self,  connector_published, connector_new_data, filter_data, time_threshold):
        self._connector_published = connector_published
        self._connector_new_data = connector_new_data
        self._time_threshold = time_threshold
        self._filter_data = filter_data
        
    @property
    def time_threshold(self):
        return self._time_threshold
        
    def __call__(self, company, limit_time_window, threshold=0.03, incr=0.01):
        # last time published
        start_time_window, end_time_window = self._connector_published.last_time(company)
        if (datetime.now() - end_time_window) < self._time_threshold:
            return 
        now = datetime.now()
        min_date = now - limit_time_window
        start_request_new_data = start_time_window if start_time_window > min_date else min_date
        data = self._connector_new_data.get(company, start_request_new_data, now)
        if data is None or ((data.index[-1] - end_time_window) >= self._time_threshold):
            data_to_publish = self._filter_data(data['close'], threshold, incr)
            self._connector_published.publish(company, data_to_publish)
            
if __name__ == '__main__':
    from src.publish_instagram.need_publish.app.publish import PublishApp
    from src.publish_instagram.need_publish.infraestructure.publish_mongodb_local_connector import MongoDBLocalConnector
    from src.read_database.stock_data import StockDataFromDataBase
    from src.publish_instagram.need_publish.domain.filter_data import filter_significative_changes
    from datetime import timedelta
    connector_new_data = StockDataFromDataBase.dailyadj_dataframe()
    connector_published = PublishApp(MongoDBLocalConnector())
    filter_data = filter_significative_changes
    time_threshold = timedelta(days=1)
    need_publish = NeedPublish(connector_published, connector_new_data, filter_data, time_threshold)
    need_publish('AAPL', timedelta(days=8))