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

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/home.html')
def student():
    return render_template('studentHome.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/bankerlogin.html', methods=["GET"])
def loginS():
    return render_template('bankerlogin.html')

@app.route('/bankerlogin.html', methods=["POST"])
def loginSGo():
    email = request.form['Email']
    password = request.form['Password']
    query = text("SELECT bank_account_id FROM banker WHERE Email = :email AND Password = :password")
    user = conn.execute(query, {'email': email, 'password': password}).fetchone()
    if user:
        global BankID
        BankID = user[0]
        query = text("SELECT First_Name FROM banker WHERE bank_account_id = :bank_account_id")
        name = conn.execute(query, {'BankID' : BankID}).fetchone()
        return render_template('bankerlogin.html', name=name[0])
    else:
        return render_template('bankerlogin.html')
    
    
@app.route('/pendingAccounts.html')
def accountsS():
    query = text("SELECT Cuser_ID, First_Name, Last_Name, Email FROM request_Cuser")
    CuserData = conn.execute(query)

    return render_template('pendingAccounts.html', CuserData=CuserData)
