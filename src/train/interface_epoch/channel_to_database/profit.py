from src.train.database.results.agents.create import CreateResultTrainDataBase
from src.train.database.results.agents.update import UpdateResultTrainDataBase
from src.train.orders.database.agents.update.id_results_train import UpdateIdResultsTrainAgentTrain

class ProfitEpoch:

    def __init__(self, source_data, train_id, stock_name):

        self._results_id = None
        self.source_data = source_data
        self.stock_name = stock_name
        self.train_id = train_id

    @property
    def stock_name(self):
        return self._stock_name

    @stock_name.setter
    def stock_name(self, stock_name):
        self._create_train_results = CreateResultTrainDataBase(stock_name)
        self._update_train_results = UpdateResultTrainDataBase(stock_name)
        self._create_reference_in_orders_db = UpdateIdResultsTrainAgentTrain(stock_name)
        self._stock_name = stock_name


    def __call__(self, epoch, env):
        return self._create_results_in_db(env.states_actions.historic_profit, epoch) if epoch == 1 \
            else self._update_results_in_db(env.states_actions.historic_profit, epoch)

    def _create_results_in_db(self, historic_profit, epoch):
        self._results_id, _ = self._create_train_results({'source_data' : self.source_data, 
                                                         f'epoch {epoch}' : {'profit' : historic_profit}}
                                                        ) 
        self._make_reference()

    def _update_results_in_db(self, historic_profit, epoch):
        self._update_train_results.update_on_id(self._results_id, 
                                                {f'epoch {epoch}' : {'profit' : historic_profit}})

    def _make_reference(self):
        return getattr(self._create_reference_in_orders_db, 
                       f'update_{self.source_data}_id_results')(self.train_id , self._results_id)
