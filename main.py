from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:jedi4890@localhost/manage_banking"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def start():
    return render_template('base.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/adminLogin.html')
def adminLogin():
    return render_template('adminLogin.html')

@app.route('/signup.html')
def adminlogin():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)