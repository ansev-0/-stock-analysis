from bson.binary import Binary
from src.tools.path import get_financial_path
import pickle
import os, json
from pymongo.errors import ServerSelectionTimeoutError

def encode_array_to_mongodb(array):
    return Binary(pickle.dumps(array, protocol=2), subtype=128)

def decode_array_from_mongodb(array):
    return pickle.loads(array)

def restart_connect_mongodb():
    with open(os.path.join(get_financial_path(), 'config.json')) as file:
        password = json.load(file)['password']
    return os.system(f'echo {password} | sudo -S -k mongod --dbpath /var/log/mongodb')


def try_except_server_selection_time_error(self, function, n):
    
    for _ in range(n):
        try:
            return function()
        except ServerSelectionTimeoutError as error:
            pass

