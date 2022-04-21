from pymongo import MongoClient

def db_info():
    HOST = 'cluster0.tznwm.mongodb.net'
    USER = 'dbuser'
    PASSWORD = '4dKC2ev6EYZ2xFSd'
    DATABASE_NAME = 'Tweet_Database'
    return HOST, USER, PASSWORD, DATABASE_NAME

def db_connect(MONGO_URI, DATABASE_NAME, COLLECTION_NAME):
    client = MongoClient(MONGO_URI)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    return collection