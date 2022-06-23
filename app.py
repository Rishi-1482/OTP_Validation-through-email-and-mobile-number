from twilio.rest import Client
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mail import Mail, Message
from random import *
app = Flask(__name__)

app.secret_key = 'thisisasecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'sampletest1482@gmail.com'
app.config['MAIL_PASSWORD'] = 'rgrrktyujzfmfzxk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    return render_template('phone.html')


@app.route('/email', methods=['GET', 'POST'])
def email():
    return render_template('email.html')


@app.route('/verifyphone', methods=['GET', 'POST'])
def verifyphone():
    msg = ''
    if request.method == 'POST':
        phone = request.form['phone']
        sentotp = getOTPFromAPI(phone)
        if sentotp:
            return render_template('verifyphone.html', name=phone, msg=msg)
        else:
            return render_template('phone.html', msg=msg)
    else:
        request.method == 'GET'
        return render_template('phone.html', msg=msg)


@app.route('/verifyOTP', methods=['POST', 'GET'])
def verifyOTP():
    if request.method == 'POST':
        enterOTP = request.form['enterOTP']
        if 'Response' in session:
            key = session['Response']
            session.pop('Response', None)
            msg = 'No'
            if key == enterOTP:
                msg = 'Valid OTP'
            else:
                msg = 'Invalid OTP'
            return render_template('verifyphone.html', msg=msg)
    else:
        return render_template('verifyphone.html')


def generateOTP():
    return randint(0000, 9999)


def getOTPFromAPI(phone):
    account_sid = 'ACc4b4d80fdccac1835e3ca0a701524e50'
    auth_token = '7f1f35ad95acc02c57aa671cae1544e0'
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['Response'] = str(otp)
    message = client.messages.create(
        from_='+19785408050',
        body="Your otp to login is " + str(otp),
        to=phone
    )

    if message.sid:
        return True
    else:
        False


@app.route('/verifyemail', methods=['POST', 'GET'])
def verifyemail():
    text = ''
    email = request.form['email']
    otp = randint(0000, 9999)
    session['Response'] = str(otp)
    msg = Message(subject='OTP', sender='rishi.enguala@gmail.com', recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('verifyemail.html', text=text)


@app.route('/validate', methods=['POST', 'GET'])
def validate():
    text = ''
    user_otp = request.form['enterOTP']
    if 'Response' in session:
        key = session['Response']
        session.pop('Response', None)
        if key == user_otp:
            return 'Valid OTP'
        else:
            return 'Invalid OTP'


if __name__ == '__main__':
    app.run(debug=True)
