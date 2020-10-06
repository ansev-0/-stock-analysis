#tasks objects
from src.models.request.agents.q_learning.tasks_for_request.based_on import BasedOnTask
from src.models.request.agents.q_learning.tasks_for_request.dates_limits import DatesLimitsTask
from src.models.request.agents.q_learning.tasks_for_request.id import IdTask
from src.models.request.agents.q_learning.tasks_for_request.path import PathTask
from src.models.request.agents.q_learning.tasks_for_request.reward import RewardTask
from src.models.request.agents.q_learning.tasks_for_request.states_actions_parameters import StatesActionParametersTask
from src.models.request.agents.q_learning.tasks_for_request.stock_data import StockDataTask
from src.models.request.agents.q_learning.tasks_for_request.stock_name import StockNameTask
#create in db objects
from src.models.database.agents.create.train_order import CreateTrainOrderAgent
#form
from src.models.request.agents.q_learning.form import FormQlearning
#class
class MakeQlearningRequest:
    
    def __call__(self, form_dict):
        #get valid form
        form = FormQlearning(**form_dict)
        form_dict = self._form_making_tasks(form)
        return CreateTrainOrderAgent(form['stock_name'])(self._form_to_db_dict(form_dict))

    def _form_making_tasks(self, form):
        pass

    def _form_to_db_dict(self, form_dict):
        return {key : value  for key, value in form_dict.items()
                if key != 'stock_name'}