from src.publish_instagram.need_publish.local_add_description import add_description_run
from src.publish_instagram.need_publish.local_need_publish import run_local_need_publish


def run():
    run_local_need_publish(['TWTR', 'AAPL', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AMZN', 
                            'AMD', 'NFLX', 'NVDA', 'MSFT', 'PYPL', 'EBAY', 
                            'ADBE', 'ADSK', 'CERN', 'EA', 'GOOG', 'QCOM', 'MCHP'])
    return add_description_run({})

    