from flask import Flask, render_template, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient

app = Flask(__name__)
app.config('JWT_SECRET_KEY') = 'jungle_note_setret'

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