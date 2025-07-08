from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_csrf_token
)
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient



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

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_note"]
users = db["users"]

@app.route('/')
def root():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({ 'username': username })
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
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if users.find_one({ 'username': username }):
        return jsonify({ 'success': False, 'msg': '이미 존재하는 아이디입니다.' })

    hashed_pw = generate_password_hash(password)

    users.insert_one({
        'name': name,
        'username': username,
        'email': email,
        'password': hashed_pw,
        'created_at': datetime.now(timezone.utc)
    })

    return jsonify({ 'success': True, 'msg': '회원가입 완료!' })

@app.route('/main', methods=['POST'])
@jwt_required()
def main():
   user = get_jwt_identity()
   return f"{user}님 환영합니다!"
     
   
        
   

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()
    access_token = create_access_token(identity=user)
    response = jsonify({ 'refresh': True })
    set_access_cookies(response, access_token)
    return response
 
@app.route('/repeat')
def repeat():
   return 'This is repeat page!'

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)