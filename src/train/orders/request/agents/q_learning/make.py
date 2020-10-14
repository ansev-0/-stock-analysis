#tasks objects
from src.train.orders.request.agents.q_learning.tasks_for_request.based_on import BasedOnTask
from src.train.orders.request.agents.q_learning.tasks_for_request.conf_build_agent.conf_build_agent import ConfBuildAgentTask
from src.train.orders.request.agents.q_learning.tasks_for_request.id import IdTask
from src.train.orders.request.agents.q_learning.tasks_for_request.path import PathTask
from src.train.orders.request.agents.q_learning.tasks_for_request.reward import RewardTask
from src.train.orders.request.agents.q_learning.tasks_for_request.states_actions_parameters import StatesActionParametersTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_data import StockDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.stock_name import StockNameTask
from src.train.orders.database.agents.create.train_order import CreateTrainOrderAgent
from src.train.orders.request.agents.q_learning.form import FormQlearning
#class
class MakeQlearningRequest:

    _make_stock_name_task = StockNameTask()
    _make_stock_data_task = StockDataTask()
    _make_reward_task = RewardTask()
    _make_states_action_parameters_task = StatesActionParametersTask()
    _make_based_on_task = BasedOnTask()
    _make_path_task = PathTask()
    _make_id_task = IdTask()
    
    def __init__(self):

        self._cache_id_train = None
        self._cache_id_validation = None
        self._path_model = None

    def __call__(self, form_dict):
        #get valid form
        form = FormQlearning(**form_dict)
        try:
            valid_form_dict = self._form_making_tasks(form)
        except Exception:
            self._remove_cache_if_errors()
        else:
            return CreateTrainOrderAgent(form['stock_name'])(**self._form_to_db_dict(valid_form_dict))
        return None


    def _remove_cache_if_errors(self):

        if self._cache_id_train is not None:
            self._make_stock_data_task.remove(self._cache_id_train)
        if self._cache_id_validation is not None:
            self._make_stock_data_task.remove(self._cache_id_validation)
        if self._path_model is not None:
            PathTask().remove(self._path_model)

    def _form_making_tasks(self, form):

        # make stock name task
        self._make_stock_name_task(form['stock_name'])
        # make stock data task
        self._cache_id_train, self._cache_id_validation = self._make_stock_data_task(
             **{key : value for key, value in form.items()
                if key in ('stock_name', 'data_train_limits',
                           'data_validation_limits', 'delays')}
            )
        # save cache_id
        form['cache_id_train'], form['cache_id_validation'] = self._cache_id_train, self._cache_id_validation
        # make reward task
        form['rewards'] = self._make_reward_task(form['rewards'], self._cache_id_train)
        form['rewards_not_done'] = self._make_reward_task(form['rewards_not_done'], self._cache_id_train)
        # make states action task
        form['train_states_actions'] = self._make_states_action_parameters_task(form['train_states_actions'],
                                                                                self._cache_id_train)
        form['validation_states_actions'] = self._make_states_action_parameters_task(form['train_states_actions'], 
                                                                                     self._cache_id_validation)
        # make based on task
        form['based_on'] = self._make_based_on_task(form['based_on'])
        # make path model task
        form['path'] = self._make_path_task(form['stock_name'], form['based_on'])
        # make id task
        form['_id'] = self._make_id_task()

        # make conf build agent task
        form['conf_build_agent'] = ConfBuildAgentTask(form['_id'],
                                                      form['stock_name'],
                                                      self._cache_id_train, 
                                                      self._cache_id_validation)(form['conf_build_agent'])
        return form

    def _form_to_db_dict(self, form_dict):
        return {key : value  for key, value in form_dict.items()
                if key != 'stock_name'}
