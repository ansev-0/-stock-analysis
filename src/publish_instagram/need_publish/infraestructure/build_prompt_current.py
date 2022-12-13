from datetime import datetime
import json
import pandas as pd

def build_prompt_current(data):
    
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    name = data['name']
    data_s = data['data']
    max_date = df.index.max().strftime(format="%b %d %Y")
    min_date = df.index.min().strftime(format="%b %d %Y")
    today = datetime.now()
    today = today.strftime("%b %d %Y")
    data_json = json.dumps(data_s)
    return f'''Next json {data_json} show {name} stock price behaviour from {min_date} to {max_date}, Today is {today}, could you write a instagram feed description new describing percentage changes between from {min_date} to {max_date}?'''
    