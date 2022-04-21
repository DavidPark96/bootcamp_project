from flask import Flask, render_template, request, flash, redirect
import mongodb #mongodb uri 정보
import db_drop #collection drop
import db_predict #crawl_tweet.py에서 데이터 크롤링 후 감성분석해서 DB에 삽입
import db_word #문장에서 단어 추출 후 새로운 'word_count' 컬렉션에 저장 

def create_app():

    app = Flask(__name__)

    app.secret_key = 'some_secret' #flash 사용하려면 필요.

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            word = request.form.get("word", type=str)
        
            # if word == "":
            #     flash("Please Input word")
            #     return render_template("get_keyword.html")
            # else:
            #기존 collection 삭제
            collection_name = 'sentiment_analysis'
            db_drop.drop_collection(collection_name)

            #새 collection 생성
            keyword = word # 입력받은 키워드
            number = 100 #검색하고 싶은 개수 
            full_text = db_predict.crawl_data(keyword, number) #크롤링
            db_predict.predict(full_text, collection_name) #감성분석 후 DB에 컬렉션 생성 후 데이터 삽입

            #단어 추출
            db_word.word_list(collection_name)
            return redirect('/dashboard')

        return render_template("get_keyword.html")

    @app.route('/dashboard')
    def test():
        return render_template('dashboard.html')

    return app