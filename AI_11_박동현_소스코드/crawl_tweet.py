from tqdm import tqdm
import pandas as pd
import tweepy
import mongodb
from pytz import timezone
from datetime import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler({'apscheduler.timezone':'Asia/seoul'})

def get_api():
    consumer_key = 'GYlEKDqrbk4pO8RJui9gLbktY'
    consumer_secret = 'XDYiQnsQWXMoNBs9csft87RorsynG3P7ZJSCjQ4S1MQnCkwcJW'
    access_token = '1511156970874544128-pzo7OM2L8TEm4hjzrfsQurgXuEzDJc'
    access_token_secret = '1wXpKasH0DJxm42ftD0MmDq1rOqiLEJ2r2XO4P3bIBxmQ'

    # 1. 핸들러 생성 및 개인정보 인증요청
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
    # 2. 액세스 요청
    auth.set_access_token(access_token, access_token_secret)
    
    # 3. twitter API 생성
    api = tweepy.API(auth,wait_on_rate_limit=True)
    # api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def get_data(keyword, number):
    api = get_api()
    tweets = tweepy.Cursor(api.search_tweets, q = keyword, tweet_mode = "extended").items(number)

    results = []
    for tweet in tqdm(tweets):
        results.append(tweet._json)
    return results

def get_time(result):
    KST = timezone('Asia/Seoul')
    utc = timezone('UTC')

    created_at = datetime.strptime(result['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    utc_created_at = utc.localize(created_at)
    kst_created_at = utc_created_at.astimezone(KST)
    date = kst_created_at.strftime('%Y-%m-%d')
    # time = kst_created_at.strftime('%H:%M:%S')
    time = kst_created_at.strftime('%H:%M')
    return date,time

def exclude_spam(keyword,number):
    results = get_data(keyword,number)
    full_text = []
    for result in results:
        if 'retweeted_status' in result: #retweet인 경우 (데이터 중복 될 것 같으면 삭제)
            data = result['retweeted_status']
            if 'https://' in data['full_text']: #스팸 필터링 1차 : https:// 포함시 필터
                continue
            else:
                if '\n' in data['full_text']: #스팸 필터링 2차 : 줄바꿈 문자 포함 중 조건에 맞지 않는 것 필터
                    if (len(data['full_text']) / data['full_text'].count('\n')) >= 10 and data['user']['followers_count'] > 20:
                        full_text.append({
                            'id_str':data['id_str'],
                            'screen_name':result['entities']['user_mentions'][0]['screen_name'],
                            'created_at_date':get_time(data)[0],
                            'created_at_time':get_time(data)[1],
                            'full_text':data['full_text'],
                            'retweeted':1
                        })
                    else:
                        continue
                else:
                    full_text.append({
                        'id_str':data['id_str'],
                        'screen_name':result['entities']['user_mentions'][0]['screen_name'],
                        'created_at_date':get_time(data)[0],
                        'created_at_time':get_time(data)[1],
                        'full_text':data['full_text'],
                        'retweeted':1
                    })
        else:
            if 'https://' in result['full_text']: #스팸 필터링 1차 : https:// 포함시 필터
                continue
            else:
                if '\n' in result['full_text']: #스팸 필터링 2차 : 줄바꿈 문자 포함 중 조건에 맞지 않는 것 필터
                    if (len(result['full_text']) / result['full_text'].count('\n')) >= 10 and result['user']['followers_count'] > 20:
                        full_text.append({
                            'id_str':result['user']['id_str'],
                            'screen_name':result['user']['screen_name'],
                            'created_at_date':get_time(result)[0],
                            'created_at_time':get_time(result)[1],
                            'full_text':result['full_text'],
                            'retweeted':0
                        })
                    else:
                        continue
                else:
                    full_text.append({
                            'id_str':result['user']['id_str'],
                            'screen_name':result['user']['screen_name'],
                            'created_at_date':get_time(result)[0],
                            'created_at_time':get_time(result)[1],
                            'full_text':result['full_text'],
                            'retweeted':0
                        })    
    return full_text