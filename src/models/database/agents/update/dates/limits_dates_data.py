from src.models.database.agents.update.dates.dates import UpdateAgentInitEndDates
from src.models.database.agents.fields import limits_data_train, limits_data_val

class UpdateAgentLimitsDateDataTrain(UpdateAgentInitEndDates):
    _valid_fields = limits_data_train

class UpdateAgentLimitsDateDataValidation(UpdateAgentInitEndDates):
    _valid_fields = limits_data_val
        
