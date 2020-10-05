from src.models.database.model_features.agents.agents import DataBaseAgentsModelFeatures
from src.models.database.model_features.agents.inputs.input import InputModel
from src.models.database.model_features.agents.run_env.run_env import RunEnvModel
from src.models.database.model_features.agents.rewards.rewards import RewardsModel
from src.models.database.model_features.agents.learn_rule.learn_rule import LearnRuleModel
from src.models.database.model_features.agents.scalers.scalers import ScalersModel
from src.models.database.model_features.agents.epsilon_exploration.epsilon_exploration import EpsilonExplorationModel
from src.tools.reduce_tools import combine_dicts

class CreateNew(DataBaseAgentsModelFeatures):

    def __call__(self, 
                 architecture_id, 
                 input_features, 
                 run_env, 
                 rewards, 
                 learn_rule, 
                 scalers, 
                 epsilon_exploration):


        return self.collection.insert_one(

            combine_dicts(InputModel(**input_features), 
                          {'architecture_id' : architecture_id},
                          RunEnvModel(**run_env),
                          RewardsModel(**rewards), 
                          LearnRuleModel(**learn_rule), 
                          ScalersModel(**scalers), 
                          EpsilonExplorationModel(**epsilon_exploration))
        )
        


