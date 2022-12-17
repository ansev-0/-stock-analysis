from src.publish_instagram.need_publish.local_need_publish import run_local_need_publish


def run():
    run_local_need_publish(['TWTR', 'AAPL', 'GOOGL', 'AMZN', 'TSLA', 'META'])
