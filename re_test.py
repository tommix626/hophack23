from newsapi import NewsApiClient

nap = NewsApiClient(api_key='1e136b4d3edd4349bd0a0c4525b4aaa2')

print(nap.get_everything(q='US-China trade war')['articles'])
