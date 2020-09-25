from src.models.database.agents.update.dates.dates import UpdateAgentInitEndDates
from src.models.database.agents.fields import train_dates
class UpdateAgentDateTrain(UpdateAgentInitEndDates):
    _valid_fields = train_dates

