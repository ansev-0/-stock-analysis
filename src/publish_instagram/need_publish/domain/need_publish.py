
from datetime import datetime
import numpy as np

class NeedPublish:
    
    def __init__(self,  connector_published, connector_new_data, filter_data, time_threshold):
        self._connector_published = connector_published
        self._connector_new_data = connector_new_data
        self._time_threshold = time_threshold
        self._filter_data = filter_data
        
    @property
    def time_threshold(self):
        return self._time_threshold
        
    def __call__(self, company, limit_time_window, threshold=0.1, incr=0.01):
        # last time published
        start_time_window, end_time_window = self._connector_published.last_time(company)
        if (datetime.now() - end_time_window) < self._time_threshold:
            return 
        now = datetime.now()
        min_date = now - limit_time_window
        start_request_new_data = start_time_window if start_time_window > min_date else min_date
        data = self._connector_new_data.get(company, start_request_new_data, now)
        if data is None:
            return
        if (data.index.max() - end_time_window) >= self._time_threshold:
            data_to_publish = self._filter_data(data, threshold, incr)
            if not data_to_publish:
                return 
            if np.max(data_to_publish['incr'].index.get_level_values(0)) > end_time_window:
                self._connector_published.publish(company, data_to_publish)
