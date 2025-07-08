from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

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
   return render_template('main.html')

@app.route('/reminder')
def repeat():
   return 'This is repeat page!'

@app.route('/memo_add')
def memo_add():
   return render_template('memo_add.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)