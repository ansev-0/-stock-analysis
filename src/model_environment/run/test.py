from src.model_environment.rewards.reward import DictRewards
from src.model_environment.rewards.not_depend_on_inventory.monotic_rewards import MonoticCumulativeRewards
from src.model_environment.rewards.not_depend_on_inventory.reward import DictNotDependOnInventoryReward
from src.model_environment.rewards.depend_on_inventory.reward import DictDependOnInventoryReward
from src.model_environment.rewards.depend_on_inventory.mean_rewards import LastPurchasesMeanReward
from src.model_environment.actions.actions import StatesActions
from src.model_environment.run.run import RunEnvAdaptModel, OutputModelActionAdapter
from src.read_database.stock_data import StockDataFromDataBase
from src.data_preparation.tools.expand.stacked_delay import StackedSequencesFromDataFrame
import numpy as np
DELAYS = 66

reader = StockDataFromDataBase.dailyadj_dataframe()
columns_ohlcv = ['open', 'high', 'low', 'close', 'volume', 'weekday']
df = reader.get('TSLA', '01/01/2014', '03/01/2020')
df = df.assign(weekday = df.index.weekday).loc[:, columns_ohlcv]

stacker = StackedSequencesFromDataFrame(range_delays = range(1, DELAYS+2))
states_ohlcv = np.diff( stacker.array_without_nan(df), axis=1)

INIT_INVENTORY = 100
INIT_MONEY = 1000
COMMISION = 0.5
GAMMA_NOT_ACTIONS_POS = 0.1

close_values = df.loc[df.index[-states_ohlcv.shape[0] -1:], 'close']
states_actions = StatesActions(close_values[:-1], INIT_INVENTORY, INIT_MONEY , COMMISION)
monotic_train_reward = MonoticCumulativeRewards(close_values, COMMISION, GAMMA_NOT_ACTIONS_POS)
reward_1 = monotic_train_reward.get_reward(action='buy',n_stocks=1, time=states_ohlcv.shape[0]-1)
states_0 = states_ohlcv[-1, :, 3]
close_values_0 = close_values[-3:]

states_actions.time = states_ohlcv.shape[0]-1
stock_price = states_actions.stock_price
pass