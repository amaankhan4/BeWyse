import pymongo

uri = 'mongodb://localhost:27017'

client = pymongo.MongoClient(uri)

db = client['local']

user_collec = db['registered_users']

customTokens = db['custom_tokens']
