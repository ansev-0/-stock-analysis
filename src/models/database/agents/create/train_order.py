from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.agents.idtype_model import AgentIdType
from pandas import to_datetime, Timestamp
from src.models.database.agents.fields import limits_data_train, limits_data_val
from src.tools.reduce_tools import flatten_adding


class CreateTrainOrderAgent(DataBaseOneAgent, AgentIdType):

    def __init__(self, stock_name, type_model, path, based_on=False):
        super().__init__(stock_name)
        self.type_model = type_model
        self.based_on = based_on
        self.path = path

    @property
    def type_model(self):
        return self._type_model

    @type_model.setter
    def type_model(self, type_model):
        if self.is_valid_type(type_model):
            self._type_model = type_model 
        raise ValueError('You must pass a valid type_model parameter')

    @property
    def based_on(self):
        return self._based_on

    @based_on.setter
    def based_on(self, based_on):
        self._based_on = based_on if self.is_valid_id_for_type_model(based_on, 
                                                                     self.type_model) \
                else False

    def __call__(self, train_limis, val_limits=None):

        self.collection.insert_one(dict(
                                        self._get_limits_dict(train_limis, val_limits),
                                        **{
                                           'status' : 'pending',
                                           'id_type' : self._get_id(),
                                           'type_model' : self.type_model,
                                           'based_on' : self.based_on,
                                           'path' : self.path
                                          }
                                       )
                   )

    def _get_id(self):
        last_id = self.get_last_id(self.type_model)
        return last_id + 1 if last_id is not None else 0
    
    def _get_limits_dict(self, limits_train, limits_val):

        if limits_val is not None:
            return dict(
                zip(
                    flatten_adding((limits_data_train, limits_data_val)),
                    map(
                        self._mapper_date_value,
                        flatten_adding((limits_train, limits_val))
                       )
                   )
            )
        return dict(
                    zip(limits_data_train, 
                        map(self._mapper_date_value, limits_train)
                        )
                    )
    # private staticmethods
    @staticmethod
    def _mapper_date_value(value):

        if isinstance(value, Timestamp):
            return value
        elif isinstance(value, str):
            return to_datetime(value)

        raise TypeError('''Invalid date Field,
                        You must pass a instance of Timestamp or str''')
