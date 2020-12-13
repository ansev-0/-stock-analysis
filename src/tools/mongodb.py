from bson.binary import Binary
import pickle

def encode_array_to_mongodb(array):
    return Binary(pickle.dumps(array, protocol=2), subtype=128)

def decode_array_from_mongodb(array):
    return pickle.loads(array)