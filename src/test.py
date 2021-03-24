from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("elasticsearch:9200", http_auth=('elastic', 'changeme'))

index_body = {
    "settings": {
        "index": { "number_of_shards": 1,  "number_of_replicas": 1 }
    },
    "mappings": {
        "properties": {
            "close" : {"type" : "float"},
            "date" : {"type" : "date"},
            "high" : {"type" : "float"},
            "low" : {"type" : "float"},
            "open" : {"type" : "float"},
            "stock_id" : {"type" : "keyword"},
            "volume" : {"type" : "integer"}
        }
  }
}

result = es.indices.create(index='history-prices-python', body=index_body)

print(result)
