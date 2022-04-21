import mongodb
def drop_collection(collection_name):
    COLLECTION_NAME = collection_name #검색할 컬렉션 이름

    HOST, USER, PASSWORD, DATABASE_NAME = mongodb.db_info()
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    collection = mongodb.db_connect(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    collection.drop()