from flask import Flask, render_template, request, redirect, url_for, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv();
app = Flask(__name__);
app.secret_key = os.getenv('SECRET_KEY');
# app.config('JWT_SECRET_KEY') = 'jungle_note_setret'

USER_DB = {
    "admin": "1234",
    "성훈": "4321"
};



client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_note"]
users = db["users"]

@app.route('/')
def root():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
   username = request.form.get('username');
   password = request.form.get('password');
   
   if username in USER_DB and USER_DB[username] == password:
      session['user'] = username
      return redirect(url_for('main'));
   else:
      return "로그인 실패! 아이디 또는 비밀번호가 틀렸습니다."

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/main')
def main():
   return 'This is main page!'

@app.route('/repeat')
def repeat():
   return 'This is repeat page!'

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)