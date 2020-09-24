from src.models.database.agents.update.dates.dates import UpdateAgentInitEndDates

class UpdateAgentLimitsDateDataTrain(UpdateAgentInitEndDates):
    _valid_fields = ('init_data_train','end_data_train') 

class UpdateAgentLimitsDateDataValidation(UpdateAgentInitEndDates):
    _valid_fields = ('init_data_val','end_data_val') 
        
