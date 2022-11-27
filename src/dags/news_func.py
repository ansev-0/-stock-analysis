from src.acquisition.to_database.tiingo.news import TiingoToDBNews
from src.acquisition.to_database.flags.news.news_last_updated import LastUpdateNews
from datetime import datetime
import pandas as pd
from src.assets.database.find import FindAssetInDataBase
import time

#
def news_func(**kwargs):
    tiingo_news = TiingoToDBNews()
    for ticker in list(map(lambda x: x['label'], FindAssetInDataBase().many(False, {}))):
        date1 = LastUpdateNews(ticker)()
        date_range = pd.date_range(str((date1).date()), str(datetime.now().date()))
        print(f'Searching with ticker : {ticker}')
        for d1, d2 in zip(date_range[:-1], date_range[1:]):
            print(d1, d2)
            tiingo_news(tickers=[ticker],
                        tags=[],
                        sources=[],
                        startDate=d1,
                        endDate=d2,
                        limit=1000, 
                        onlyWithTickers=True)

        time.sleep(0.1)
    return 'Done'   
