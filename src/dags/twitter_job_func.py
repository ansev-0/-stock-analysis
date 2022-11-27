
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.manager import JobManager
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient
import argparse
import os

def twitter_job():
    manager = JobManager()

    def decode_arg(arg):
        if arg == 'None':
            return None
        elif arg is None:
            return arg
        else:
            return int(arg)
    #call

    manager(task={'word' : 'apple', 
                  '_id' : '0', 
                  'since_id' : None, 
                  'max_id' : None})
#if __name__ == '__main__':
#    twitter_job()




