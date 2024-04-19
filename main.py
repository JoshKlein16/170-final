from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:jedi4890@localhost/manage_banking"
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

@app.route('/transfer.html', methods=["GET"])
def transfer():
    return render_template('transfer.html')

@app.route('/transfer', methods=["POST"])
def transfer_money():
    recipient_account_id = request.form['recipient_account_id']
    amount = float(request.form['amount'])

    recipient_query = text("SELECT * FROM users WHERE bank_account_id = :recipient_account_id")
    recipient = conn.execute(recipient_query, {'recipient_account_id': recipient_account_id}).fetchone()

    if recipient:
        global BankID
        BankID = recipient[0]
        user_query = text("SELECT balance FROM users WHERE bank_account_id = :user_account_id")
        user_balance = conn.execute(user_query, {'user_account_id': BankID}).fetchone()[0]

        if user_balance >= amount:
            new_user_balance = user_balance - amount

            update_user_query = text("UPDATE users SET balance = :new_balance WHERE bank_account_id = :user_account_id")
            conn.execute(update_user_query, {'new_balance': new_user_balance, 'user_account_id': BankID})

            new_recipient_balance = recipient[1] + amount

            update_recipient_query = text("UPDATE users SET balance = :new_balance WHERE bank_account_id = :recipient_account_id")
            conn.execute(update_recipient_query, {'new_balance': new_recipient_balance, 'recipient_account_id': recipient_account_id})

            return "Money transferred successfully."
        else:
            return "Insufficient balance."
    else:
        return "Recipient account not found."

if __name__ == '__main__':
    app.run(debug=True)