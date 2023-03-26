import certifi
from bson.objectid import ObjectId
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)
ca = certifi.where()
client = MongoClient(
    'mongodb+srv://sparta:sparta@cluster0.1dpm6q3.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogdescription = soup.select_one(
        'meta[property="og:description"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': ogtitle,
        'description': ogdescription,
        'image': ogimage,
        # 'url': url_receive,
        'comment': comment_receive,
        'star': star_receive
    }
    db.movies.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@ app.route("/movie", methods=["GET"])
def movie_get():
    comments = list(db.movies.find())
    # convert ObjectId to string
    comments = [{**comment, **{"_id": str(comment["_id"])}}
                for comment in comments]
    return jsonify({'result': comments})


@app.route("/movie", methods=["DELETE"])
def movie_delete():
    delete_receive = request.form["id"]
    db.movies.delete_one({'_id': ObjectId(delete_receive)})
    return jsonify({'result': "success"})


if __name__ == '__main__':
    app.run()
