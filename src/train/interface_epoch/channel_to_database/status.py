from src.train.orders.database.agents.update.status import UpdateStatusAgentTrain
from src.train.orders.database.agents.find import FindTrainAgent
from src.train.orders.database.agents.update.start_end_train import UpdateStartEndAgentTrain

class TrainAgentStatus:

    def __init__(self, stock_name, train_id):
        self.stock_name = stock_name
        self.train_id = train_id

    def __call__(self, epoch):
        if epoch == 1:
            return self._set_running()
        elif epoch == self._total_epochs:
            return self._set_done()
        return None

    @property
    def stock_name(self):
        return self._stock_name

    @property
    def train_id(self):
        return self._train_id

    @train_id.setter
    def train_id(self, train_id):
        self._train_id = train_id
        self._total_epochs = self._make_order_request()['conf_build_agent']['epochs']

    @stock_name.setter
    def stock_name(self, stock_name):
        self._set_running = UpdateStatusAgentTrain.set_running(stock_name)
        self._set_done = UpdateStatusAgentTrain.set_done(stock_name)
        self._set_dates = UpdateStartEndAgentTrain(stock_name)
        self._find_order = FindTrainAgent(stock_name)
        self._stock_name = stock_name

    def _set_running(self, epoch):
        return self._set_running.set_on_id(self.train_id), self._set_dates('start_date_train')

    def _set_done(self, epoch):
        return self._set_done.set_on_id(self.train_id), self._set_dates('end_date_train')

    def _make_order_request(self):
        return self._find_order.by_train_id(self._train_id, 
                                            projection={'conf_build_agent' : 1})
