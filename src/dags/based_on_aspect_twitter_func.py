''' Module to search new text to analyze from twitter'''

from pymongo import MongoClient
from datetime import datetime
#import aspect_based_sentiment_analysis as absa
import pandas as pd
import numpy as np
from src.assets.database.find import FindAssetInDataBase
from functools import reduce
from src.acquisition.to_database.tiingo.saver.news import SaverTiingoNewsFromDataFrame

# func to search in database from text without field analyze
# func to analyze
# func to save
#saver = SaverTiingoNewsFromDataFrame()

def read_dataframe_twitter(company):
    # check if empty collection
    if company not in MongoClient()['twitter_search_assets'].list_collection_names():
        return None
    collection = MongoClient()['twitter_search_assets'][company]
    if not collection.count_documents({}):
        return None
    df = pd.DataFrame.from_dict({key : value for doc in collection.find({}) 
                                 for key, value in doc.items() 
                                 if key != '_id'}, orient='index')
    return df

def analyze_serie_with_label(serie, label, nlp):

    serie = serie.str.lower()
    label = label.lower()
    serie_filtered = serie.loc[serie.str.contains(label)]
    if serie_filtered.empty:
        return None
    return serie.to_frame(serie.name).join(
        pd.DataFrame(serie_filtered.apply(lambda text: nlp(text, 
                                                           aspects=[label]).examples[0].scores).tolist(), 
                     columns=list(map(lambda text: f'{serie.name}_{label}_sentiment_{text}', 
                                      ('neutral', 'negative', 'positive'))), 
                     index=serie_filtered.index), how='left').fillna(0)

def filter_already_analyzed(df, label, field):
    if not any([f'{field}_{label}' in col for col in df.columns]):
        return df
    return df.loc[df.filter(regex=f'{field}_{label}').isnull().any(axis=1)]

def update_news_from_dataframe(df, label):
    dicts_to_update = [dict({'_id' : pd.to_datetime(date)}, **group.to_dict('index')) 
                       for date, group in df.groupby(pd.to_datetime(df.index.to_series()).dt.date)]
    for dict_ in dicts_to_update:                   
        MongoClient()['twitter_search_assets'][label].update_one({'_id' : dict_['_id']}, {'$set' : dict_}, upsert=True)


def based_aspect_twitter_analysis_func():

    import tensorflow as tf
    from tensorflow.compat.v1.keras.backend import set_session
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
    config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                # (nothing gets printed in Jupyter, only if you run it standalone)
    sess = tf.compat.v1.Session(config=config)
    set_session(sess)  # set this TensorFlow session as the default session for Keras
    import aspect_based_sentiment_analysis as absa
    nlp = absa.load()

    # search assets
    assets = list(FindAssetInDataBase().many(False, {}))
    print(assets)   
    # read dataframe    
    #df = read_dataframe_tiingo_news('AAPL')   
    #fields
    valid_fields = ('full_text', )
    # para cada asset
    print('INIT TASK')
    for dict_asset in assets:
        features = reduce(lambda cum_list, new_item: cum_list + new_item 
                                                    if isinstance(new_item, list) 
                                                    else cum_list + [new_item], 
                          [value.lower() for key, value in dict_asset.items() 
                           if key != '_id' and isinstance(value, str)], [])
        df = read_dataframe_twitter(dict_asset['label'])
        if df is None:
            continue
    # para cada caracteristica
        for feature in features:
            print(feature)
            # para cada campo
            for field in valid_fields:
                print(field)
                df_to_analysis = filter_already_analyzed(df, feature, field)
                df_analysis = analyze_serie_with_label(df_to_analysis[field], feature, nlp)
                if df_analysis is None:
                    continue
                df = df.combine_first(df_analysis)
                update_news_from_dataframe(df, dict_asset['label'])





