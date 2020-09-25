from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB
from src.models.database.agents.fields import path

class UpdateAgentPath(DataBaseOneAgent, UpdateValidFieldsDocumentDB):
    
    _valid_fields = ('path', )
    @property
    def valid_fields(self):
        return self._valid_fields
