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
    conn.execute(text("INSERT INTO request_Cuser (First_Name, Last_Name, Email, Password, Phone_Number, SSN, checking) VALUES (:fName, :lName, :email, :password, :phone, :ssn, '0')"),  request.form)
    conn.commit()
    return render_template("index.html")

@app.route('/home.html')
def student():
    return render_template('index.html')



@app.route('/pendingAccounts.html')
def accounts():
    query = text("SELECT Cuser_ID, First_Name, Last_Name, Email, Phone_Number, SSN FROM request_Cuser")
    CuserData = conn.execute(query)

    return render_template('pendingAccounts.html', CuserData=CuserData)




@app.route('/bankerlogin.html', methods=["GET"])
def loginS():
    return render_template('bankerlogin.html')

@app.route('/bankerlogin.html', methods=["POST"])
def loginSGo():
    email = request.form['Email']
    password = request.form['Password']
    query = text("SELECT Cuser_ID FROM banker WHERE Email = :email AND Password = :password")
    user = conn.execute(query, {'email': email, 'password': password}).fetchone()
    if user:
        global BankID
        BankID = user[0]
        query = text("SELECT First_Name, FROM banker WHERE Cuser_ID = :Cuser_ID")
        name = conn.execute(query, {'Cuser_ID' : BankID}).fetchone()
        return render_template('adminpanel.html', name=name[0])
    else:
        return render_template('bankerlogin.html')
    
@app.route('/login.html', methods=["GET"])
def login():
    return render_template('login.html')

@app.route('/login.html', methods=["POST"])
def loginGo():
    email = request.form['Email']
    password = request.form['Password']
    query = text("SELECT Cuser_ID FROM Cuser WHERE Email = :email AND Password = :password")
    user = conn.execute(query, {'email': email, 'password': password}).fetchone()
    if user:
        global BankID
        BankID = user[0]
        query = text("SELECT First_Name FROM Cuser WHERE Cuser_ID = :Cuser_ID")
        name = conn.execute(query, {'Cuser_ID': BankID}).fetchone()
        # GetInfo = text("SELECT First_Name, Last_Name, Email, Password, Phone_Number, SSN, checking FROM banker WHERE Cuser_ID = :Cuser_ID")
        # accountInfo = conn.execute(GetInfo, {'Cuser_ID': BankID}).fetchone()
        if name:
            return render_template('home.html', name=name[0])
        else:
            return render_template('home.html', name="WHO DF ARE YOU")
    else:
        return render_template('index.html')
    

@app.route('/ViewAccount.html')
def ViewAccount():
    query = text("SELECT First_Name, Last_Name, Email, Password, Phone_Number, SSN, checking FROM Cuser WHERE Cuser_ID = :Cuser_ID")
    accountInfo = conn.execute(query, {'Cuser_ID': BankID}).fetchone()

    return render_template('ViewAccount.html', AccountData=accountInfo)





























if __name__ == '__main__':
    app.run(debug=True)