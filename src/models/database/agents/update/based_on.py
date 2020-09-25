from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.agents.idtype_model import AgentIdType
from src.models.database.update import UpdateValidFieldsDocumentDB
from src.models.database.agents.fields import based_on

class UpdateAgentBasedOnId(DataBaseOneAgent, UpdateValidFieldsDocumentDB, AgentIdType):

    _valid_fields = based_on

    @property
    def valid_fields(self):
        return self._valid_fields

    def based_on(self, type_model, id_type, based_on_id, **kwargs):

        self._check_valid_based_on_id(type_model, based_on_id)
        self.update_one({'type_model' : type_model,
                         'id_type' : id_type},
                        {'based_on_id', based_on_id}, **kwargs)


    def _check_valid_based_on_id(self, type_model, id_type):
        if not self.is_valid_id_for_type_model(id_type, type_model):
            raise ValueError(f'''Invalid id_type: {id_type}
                             for type_model : {type_model}''')
        
        