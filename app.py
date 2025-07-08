from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config('JWT_SECRET_KEY') = 'jungle_note_setret'

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_note"]
users = db["users"]

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
   return 'This is main page!'

@app.route('/repeat')
def repeat():
   return 'This is repeat page!'

if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)