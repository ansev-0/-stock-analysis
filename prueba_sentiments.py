import importlib_metadata as metadata
import sys
for k,v in sys.path_importer_cache.items():
    if not v:
        print(k)
        print('now')
print('\n-'.join(sys.path))
for i in metadata.distributions():
    print(i.name)
    if not i.name:
        print('now')
    #print(i)
import tensorflow as tf
from tensorflow.python.keras import backend as K
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
#config.gpu_options.per_process_gpu_memory_fraction=0.9

                            # (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.compat.v1.Session(config=config)
K.set_session(sess)
import aspect_based_sentiment_analysis as absa
import pandas as pd
K.set_session(sess)

nlp = absa.load()
i=0
def text_sentiment_based(text, list_aspects):
    global i
    i+=1
    print(i)
    return list(map(str, nlp((text), aspects=list_aspects).examples[0].scores))

text_sentiment_based('amzn is great', ['amzn', 'is'])

print(pd.DataFrame(['hola']))