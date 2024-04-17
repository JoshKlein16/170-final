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

@app.route('/adminLogin.html', methods=["POST"])
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
        return render_template('adminView.html', name=name[0])
    else:
        return render_template('adminLogin.html')

@app.route('/transfer.html')
def transferPage():
    return render_template('transfer.html')

@app.route('/transfer', methods=['POST'])
def transfer():
    sender_account_number = int(request.form['sender_account_number'])
    receiver_account_number = int(request.form['receiver_account_number'])
    amount = float(request.form['amount'])

    # Validate the sender and receiver account numbers
    sender_query = text("SELECT * FROM users WHERE bank_account_id = :account_number")
    sender = conn.execute(sender_query, {'account_number': sender_account_number}).fetchone()
    receiver_query = text("SELECT * FROM users WHERE bank_account_id = :account_number")
    receiver = conn.execute(receiver_query, {'account_number': receiver_account_number}).fetchone()

    if not sender or not receiver:
        return 'Invalid account number'

    # Check if the sender has sufficient balance for the transaction
    if sender['balance'] < amount:
        return 'Insufficient balance'

    # Debit the sender's account and credit the receiver's account
    debit_query = text("UPDATE users SET balance = balance - :amount WHERE bank_account_id = :account_number")
    conn.execute(debit_query, {'amount': amount, 'account_number': sender_account_number})
    credit_query = text("UPDATE users SET balance = balance + :amount WHERE bank_account_id = :account_number")
    conn.execute(credit_query, {'amount': amount, 'account_number': receiver_account_number})
    conn.commit()

    return 'Transfer successful'

if __name__ == '__main__':
    app.run(debug=True)