from src.crontab_tasks.create_task import CreateRunTaskCronTab
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.create import CreateTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.job import CronTwitterJob
from datetime import datetime

class CreateNewJob(CronTwitterJob):
    
    _cron_tasks = CreateRunTaskCronTab()
    _db_create = CreateTwitterApiJobsDataBase()
    

    def one(self, 
            dict_job, 
            #datetime
        ):
        dict_job['_id'] = self._new_id
        # create in db
        self._db_create.one(dict(dict_job, **{
                                              #'date' : datetime, 
                                              #'_id' : dict_job['_id'], 
                                              'last_update' : datetime.now(),
                                              'created_at' : datetime.now()}))
        # create cron job
        #args_job = self._get_args(dict_job)
        #self._cron_tasks.add_datetime_task(f'{self._name_cron_job} {args_job}', datetime)
        ## write job
        #self._cron_tasks.write()

#from src.assets.database.find import FindAssetInDataBase
#assets = FindAssetInDataBase().many(False, {})


#from pymongo import MongoClient
#companies = MongoClient()['acquisition_orders']['stock_data_intraday'].find_one({'_id' : 'alphavantage'})['orders']
#create = CreateNewJob()
#for company in assets:
#    create.one(dict_job={'word' : company['name'], 'since_id' : None, 'max_id' : None, 'factor_priority' : 900, 'status' : 'pending'})
#    create.one(dict_job={'word' : company['label'], 'since_id' : None, 'max_id' : None, 'factor_priority' : 900, 'status' : 'pending'})