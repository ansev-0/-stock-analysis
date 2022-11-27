from tiingo import TiingoClient
import json
import os

def get_client():
    with open(os.path.join('filestore', 'credentials', 'tiingo', 'token.json')) as f:
        config={}
        # To reuse the same HTTP Session across API calls (and have better performance), include a session key.
        config['session'] = True
        config['api_key'] = list(json.load(f).values())[0]
        client = client = TiingoClient(config)
    return client