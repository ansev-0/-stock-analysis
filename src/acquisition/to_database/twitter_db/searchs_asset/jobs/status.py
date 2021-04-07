from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiStatusDataBase
from src.acquisition.acquisition.twitter_acquisition.twitter_request import TwitterAPIAuthJson
import os
from datetime import datetime
from tweepy.error import RateLimitError
from src.tools.path import get_financial_path

class UpdateStatusFromAPI:

    _update_status = UpdateTwitterApiStatusDataBase()
    folder = os.path.join(get_financial_path(), 'twitter_credentials')

    def __call__(self):
        for credentials in os.listdir(self.folder):
            if not credentials.endswith('.json'):
                continue
            self._update_limits(credentials)


    def _update_limits(self, credentials):
        try:
            response = TwitterAPIAuthJson(os.path.join(self.folder, credentials)).rate_limit_status()
            response = response['resources']['application']['/application/rate_limit_status']

            self._update_status.one(
                {'api_user' : credentials.replace('.json', '')},
                dict(response, 
                     **{'requests' : response['limit'] - response['remaining'], 
                        'waiting' : False, 
                        'errors_api_status' : None, 
                        'reset_api_date' : datetime.fromtimestamp(response['reset']),
                        'last_update_by_api' : datetime.now(),
                        'available_api' : True}), 
                upsert=True)

        except RateLimitError as error:

            self._update_status.one(
                {'api_user' : credentials.replace('.json', '')},
                {'remaining' : 0,
                 'waiting' : True, 
                 'errors_api_status' : None, 
                 'last_update_by_api' : datetime.now(),
                 'available_api' : True},
                upsert=True)
            
        except Exception as error:

              self._update_status.one(
                {'api_user' : credentials.replace('.json', '')},
                {'available_api' : False, 
                 'errors_api_status' : str(error), 
                 'last_update_by_api' : datetime.now()},
                upsert=True)
#git pulUpdateStatusFromAPI()()