from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_csrf_token
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import jwt

load_dotenv();
app = Flask(__name__);
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=2)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # 테스트용
SECRET_KEY = os.getenv('SECRET_KEY');
# app.config('JWT_SECRET_KEY') = 'jungle_note_setret'
jwt = JWTManager(app)

app = Flask(__name__)

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')  # Studio 3T에서 본 연결 정보
db = client['jungle_note']  # 또는 실제 사용할 DB 이름 (예: 'jungle_note')
memo_collection = db['memos', 'users']  # 사용할 컬렉션 이름

memos = []

@app.route('/')
def root():
   return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = memo_collection.find_one({ 'username': username })
    if not user:
        return jsonify({ 'success': False, 'msg': '존재하지 않는 사용자입니다.' }), 401

    if not check_password_hash(user['password'], password):
        return jsonify({ 'success': False, 'msg': '비밀번호가 틀렸습니다.' }), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    response = jsonify({
        'success': True,
        'msg': '로그인 성공!',
        'csrf_token': get_csrf_token(access_token)  # CSRF 보호를 위해 전송
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({ "logout": True })
    unset_jwt_cookies(response)  # 쿠키 제거
    return response

@app.route('/make', methods=['GET'])
def make():
   return render_template('register.html')

@app.route('/register', methods=["POST"])
def register_post():
    data = request.get_json()
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    user_email = data.get('user_email')
    user_pw = data.get('user_pw')

    if memo_collection.find_one({ 'user_id': user_id }):
        return jsonify({ 'success': False, 'msg': '이미 존재하는 아이디입니다.' })

    hashed_pw = generate_password_hash(user_pw)

    memo_collection.insert_one({
        'user_name': user_name,
        'user_id': user_id,
        'user_email': user_email,
        'user_pw': hashed_pw,
    })

    return jsonify({ 'success': True, 'msg': '회원가입 완료!' })

@app.route('/main')
@jwt_required()
def main():
   user = get_jwt_identity()
   memos = list(memo_collection.find({}, {'_id': 0}))
   return render_template('main.html', memos=memos)

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    response = jsonify({ 'refresh': True })
    set_access_cookies(response, access_token)
    return response

@app.route('/memo')
def memo():
   return render_template('memo.html')

@app.route('/reminder')
def repeat():
   return 'This is repeat page!'

@app.route('/memo_add', methods=['GET','POST'])
def memo_add():
   if request.method == 'POST':
      title = request.form['title']
      content = request.form['content']
      user_id = session['user_id']
      memo_collection.insert_one({
         'user_id': user_id,
         'title': title,
         'content': content,
         'created_at': datetime.now(),
         'repeat_visible': True  # 기본값 True
      })
      return redirect('/main')
   return render_template('memo_add.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)