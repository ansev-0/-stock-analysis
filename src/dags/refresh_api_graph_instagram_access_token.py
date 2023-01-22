from instagram_client.instagram_api.adapters.request_session_adapter import RequestsGraphInstagram
from datetime import datetime, timedelta
import json
import pandas as pd
#step 1:  request token
def refresh_access_token():

    with open('filestore/credentials/instagram/api_graph_instagram.json') as f:
        d = json.load(f)
    
    if ('max_refresh_day' in d) and (datetime.now() > pd.to_datetime(d['max_refresh_day'])):
        raise RuntimeError
    elif ('max_refresh_day' in d) and ((datetime.now() -  pd.to_datetime(d['max_refresh_day'])) < timedelta(days=10)):
        return
    r = RequestsGraphInstagram(access_token=d['access_token'])
    long_duration_response = r.get_access_token_long_duration(client_id=d['client_id'],
                                                           client_secret=d['client_secret'])
    assert long_duration_response.ok
    long_duration_json = long_duration_response.json()
    print(long_duration_json)
    d['max_refesh_day'] = (datetime.now() + timedelta(seconds=long_duration_json['expires_in'])).strftime("%m/%d/%Y, %H:%M:%S")
    d['access_token'] = long_duration_json['access_token']
    
    with open('filestore/credentials/instagram/api_graph_instagram.json', 'w') as f:
        json.dump(d, f)