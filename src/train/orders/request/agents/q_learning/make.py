#tasks objects
from src.train.orders.request.agents.q_learning.tasks_for_request.based_on import BasedOnTask
from src.train.orders.request.agents.q_learning.tasks_for_request.dates_limits import DatesLimitsTask
from src.train.orders.request.agents.q_learning.tasks_for_request.id import IdTask
from src.train.orders.request.agents.q_learning.tasks_for_request.path import PathTask
from src.train.orders.request.agents.q_learning.tasks_for_request.reward import RewardTask
from src.train.orders.request.agents.q_learning.tasks_for_request.states_actions_parameters import StatesActionParametersTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_data import StockDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_name import StockNameTask
#create itrainborders.jects
from src.train.orders.database.agents.create.train_order import CreateTrainOrderAgent
#formorders.
from src.train.orders.request.agents.q_learning.form import FormQlearning
#class
class MakeQlearningRequest:
    
    def __call__(self, form_dict):
        #get valid form
        form = FormQlearning(**form_dict)
        valid_form_dict = self._form_making_tasks(form)
        return CreateTrainOrderAgent(form['stock_name'])(self._form_to_db_dict(valid_form_dict))

    def _form_making_tasks(self, form):

        # check valid stock name
        StockNameTask()(form['stock_name'])
        cache_id_train, cache_id_val = StockDataTask()\
            (
             {key : value for key, value in form.items()
              if key in ('stock_name', 'data_train_limits',
                         'data_validation_limits', 'delays')}
            )
        # reward task
        form['rewards'] = RewardTask()(form['rewards'], cache_id_train)
        form['rewards_not_done'] = RewardTask()(form['rewards_not_done'], cache_id_train)
        # states action task
        form['train_states_actions'] = StatesActionParametersTask()(form['train_states_actions'],
                                                                    cache_id_train)
        form['validation_states_actions'] = StatesActionParametersTask()(form['train_states_actions'], 
                                                                         cache_id_val)
        return form


    def _form_to_db_dict(self, form_dict):
        return {key : value  for key, value in form_dict.items()
                if key != 'stock_name'}