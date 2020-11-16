from src.train.orders.database.agents.agents import DataBaseOneAgent
from src.database.update import UpdateValidFieldsDocumentDB

class UpdateIdResultsTrainAgentTrain(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = ('train_id_results', 'validation_id_results')

    @property
    def valid_fields(self):
        return self._valid_fields

    def update_train_id_results(self, train_id_order, train_id_results):

        return self.update_one(where={'_id' : train_id_order}, 
                               data={'train_id_results' : train_id_results})

    def update_validation_id_results(self, train_id_order, validation_id_results):
        
        return self.update_one(where={'_id' : train_id_order}, 
                               data={'validation_id_results' : validation_id_results})
