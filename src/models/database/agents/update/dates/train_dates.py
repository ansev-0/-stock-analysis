from src.models.database.agents.update.dates.dates import UpdateAgentInitEndDates

class UpdateAgentDateTrain(UpdateAgentInitEndDates):
    _valid_fields = ('init_data_train','end_data_train') 

