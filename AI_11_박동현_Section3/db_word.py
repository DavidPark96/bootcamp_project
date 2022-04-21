import mongodb
# from tqdm import tqdm
# from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Okt
# from bertopic import BERTopic
import pandas as pd

def word_list(collection_name):
    okt = Okt()
    COLLECTION_NAME = collection_name

    HOST, USER, PASSWORD, DATABASE_NAME = mongodb.db_info()
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    collection = mongodb.db_connect(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    documents = collection.find()

    clean_words = []
    for document in documents:
        for word in okt.pos(document['full_text'], stem=True): #어간 추출
            if word[1] in ['Noun', 'Adverb'] and len(word[0]) >= 2:
                clean_words.append(word[0])

    dict = [{'words': clean_words[i]} for i in range(0, len(clean_words))] #list to dict

    COLLECTION_NAME_SAVE = 'word_count'
    collection_save = mongodb.db_connect(MONGO_URI, DATABASE_NAME, COLLECTION_NAME_SAVE)
    collection_save.drop() #기존데이터 삭제
    collection_save.insert_many(dict)