import aspect_based_sentiment_analysis as absa
from pymongo import MongoClient
import pandas as pd
from functools import reduce

data = MongoClient()['tiingo_news']['AAPL'].find({})
dict_ = reduce(lambda x, y: dict(x, **y), 
           [{key:value for key, value in d.items() if key != '_id'} for d in data])
df = pd.DataFrame.from_dict(dict_, orient='index')
df = df.rename_axis(index='id').reset_index()
df['published_date'] = pd.to_datetime(df['published_date'])
df['crawl_date'] = pd.to_datetime(df['crawl_date'])


df['article'] = df['title'].str.cat(df['description'], '. ').str.lower()

nlp = absa.load()
i=0
def text_sentiment_based(text, list_aspects):
    global i
    i+=1
    print(i)
    return list(map(str, nlp((text), aspects=list_aspects).examples[0].scores))

m_apple = df['article'].str.contains('apple')
m_aapl = df['article'].str.contains('aapl') 

apple = df.loc[m_apple, 'article']
print(len(apple))
aapl = df.loc[m_aapl, 'article']
print(len(aapl))
anaylsis = text_sentiment_based(apple.iloc[0], ['apple'])
pass
df['sentiment_aapl'] = aapl.apply(lambda x: text_sentiment_based(x, ['aapl']))
i=0
df['sentiment_apple'] = apple.apply(lambda x: text_sentiment_based(x, ['apple']))

import json
df['published_date'] = df['published_date'].astype(str)
df['crawl_date'] = df['crawl_date'].astype(str)
print(df.dtypes)
with open('analysis.json', 'w+') as f:
    json.dump(df.to_dict(), f)
