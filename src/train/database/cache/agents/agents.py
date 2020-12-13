from src.train.database.cache.client_cache import DataBaseTrainCache

class DataBaseAgentTrainCache(DataBaseTrainCache):

    def __init__(self):
        super().__init__('agents')


