import os
from datetime import datetime
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()

es = Elasticsearch(os.getenv("ELASTIC_SEARCH_HOST"), http_auth=(os.getenv("ELASTIC_NAME" ), os.getenv("ELASTIC_PASSWORD")))

documents = [
    {"index":{
        "_index": 'history-prices-python',
        "_id" : "0345"}
    },
    { "stock_id":"00878", "date":"2021-03-18", "volume":2232343, "open":104.20, "high":105.35, "low":102.80, "close":104.00 },
]

result = es.bulk(body=documents, index='history-prices-python')

print(result)
