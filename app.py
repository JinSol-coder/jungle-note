from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')  # Studio 3T에서 본 연결 정보
db = client['jungle_note']  # 또는 실제 사용할 DB 이름 (예: 'jungle_note')
memo_collection = db['memos']  # 사용할 컬렉션 이름

memos = []

@app.route('/')
def root():
   return redirect(url_for('login'))

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/main')
def main():
   memos = list(memo_collection.find({}, {'_id': 0}))
   return render_template('main.html', memos=memos)

@app.route('/reminder')
def repeat():
   return 'This is repeat page!'

@app.route('/memo_add', methods=['GET','POST'])
def memo_add():
   if request.method == 'POST':
      title = request.form['title']
      content = request.form['content']
      #user_id = session['user_id']
      memo_collection.insert_one({
         #'user_id': user_id,
         'title': title,
         'content': content,
         'created_at': datetime.now(),
         'repeat_visible': True
      })
      return redirect('/main')
   return render_template('memo_add.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)