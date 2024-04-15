from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:CSET@localhost/manage_banking"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/createA.html')
def signup():
    return render_template('createA.html')

@app.route('/createA.html', methods=["GET"])
def signupT():
    return render_template("createA.html")

@app.route('/createA.html', methods=["POST"])
def createArequest():
    conn.execute(text("INSERT INTO request_Cuser (First_Name, Last_Name, Email, Password, Phone_Number, SSN) VALUES (:fName, :lName, :email, :password, :phone, :ssn)"),  request.form)
    conn.commit()
    return render_template("index.html")

@app.route('/home.html')
def student():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)