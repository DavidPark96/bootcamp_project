import kobert_predict
import crawl_tweet
import mongodb

def crawl_data(keyword, number):
    full_text = crawl_tweet.exclude_spam(keyword, number)
    print('필터링 후 데이터 크기: '+ str(len(full_text)))
    return full_text

def predict(full_text, collection_name):
    print('Predicting...')
    sentiment_analysis = []
    for document in full_text:
        document['sentiment'] = kobert_predict.predict(document['full_text']) #감성분석 결과 딕셔너리에 추가
        sentiment_analysis.append(document)

    #분석 결과 저장
    COLLECTION_NAME_SAVE = collection_name
    HOST, USER, PASSWORD, DATABASE_NAME = mongodb.db_info()
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
    collection_save = mongodb.db_connect(MONGO_URI, DATABASE_NAME, COLLECTION_NAME_SAVE)
    collection_save.insert_many(sentiment_analysis)


# keyword = '어렵' # 검색하고 싶은 키워드 입력
# number = 100 #검색하고 싶은 개수
# collection_name = 'test1'
# full_text = crawl_data(keyword, number)
# predict(full_text, collection_name)