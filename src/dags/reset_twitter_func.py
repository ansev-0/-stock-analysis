from src.acquisition.to_database.twitter_db.searchs_asset.jobs.create import CreateNewJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.delete import RemoveStatusJob
from src.assets.database.find import FindAssetInDataBase
from pymongo import MongoClient

def reset_twitter():
    RemoveStatusJob().many({})
    assets = FindAssetInDataBase().many(False, {})
    MongoClient()['crontab']['twitter_searchs_mutex'].delete_many({})
    companies = MongoClient()['acquisition_orders']['stock_data_intraday'].find_one({'_id' : 'alphavantage'})['orders']
    create = CreateNewJob()

    for company in assets:
        if company['label'] not in ('MSFT', 'GOOGL', 'GOOG', 'AMZN', 'AMD', 'NLFX', 'TWTR', 
                                    'FB', 'TSLA', 'NVDA', 'EBAY', 'ADSK'):
            continue
        if isinstance(company['name'], str):
            create.one(dict_job={'word' : company['name'], 
                                 'since_id' : None, 'max_id' : None, 
                                 'factor_priority' : 900, 'status' : 'pending'})
        if isinstance(company['label'], str):
            create.one(dict_job={'word' : company['label'], 
                                 'since_id' : None, 'max_id' : None, 
                                 'factor_priority' : 900, 'status' : 'pending'})

