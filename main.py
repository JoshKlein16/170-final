from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:Savier010523$@localhost/manage_banking"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def start():
    return render_template('base.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/home.html')
def student():
    return render_template('studentHome.html')

if __name__ == '__main__':
    app.run(debug=True)