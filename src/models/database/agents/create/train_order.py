from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.agents.type_model import AgentType
from src.models.database.dates import DatetimeDates
from src.models.database.agents.fields import limits_data_train, limits_data_val
from src.tools.reduce_tools import flatten_adding
from src.models.database.parameters.folder_of_folder_file import FolderofFolderExtFiles
from src.models.database.parameters.path import PathModels
from src.tools.reduce_tools import combine_dicts
from datetime import datetime



class CreateTrainOrderAgent(DataBaseOneAgent, AgentType):

    def __init__(self, stock_name):

        super().__init__(stock_name)
        self._folder = FolderofFolderExtFiles.agents(stock_name)

    @property
    def path(self):
        return self._folder.next_file

    @based_on.setter
    def based_on(self, based_on):
        self._based_on = based_on if self._model_exist(based_on) \
                else False

    def __call__(self, type_model, based_on, train_limis, val_limits=None):
        
        #check type model
        self._check_type_model(type_model)
        #validate based_on
        based_on = based_on if self._model_exist(based_on) \
                else False

        #create train order
        return self.collection.insert_one(

            combine_dicts(self._get_dates_dict(train_limis, val_limits),
                          self._get_not_dates_dict(type_model, based_on))
        )

    def _get_id(self):
        return datetime.now()

    def _get_not_dates_dict(self, type_model, based_on):
        return  {
                 'status' : 'pending',
                 'id_type' : self._get_id(),
                 'type_model' : type_model,
                 'based_on' : based_on,
                 'path' : self.path
                }
    
    def _get_dates_dict(self, limits_train, limits_val):

        if limits_val is not None:
            return DatetimeDates()\
                .dates_for_save_from_tuples(flatten_adding((limits_data_train,
                                                            limits_data_val)),
                                            flatten_adding((limits_train, limits_val))
                                                    
        )
        return DatetimeDates().dates_for_save_from_tuples(limits_data_train,
                                                          limits_train)

    @staticmethod
    def _model_exist(model):
        return PathModels().path_exist(model)

    def _check_type_model(self, type_model):
        if not self.is_valid_type(type_model):
            raise ValueError('You must pass a valid type_model parameter')

