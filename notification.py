#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import log_template
from flask_cors import CORS

import os, sys
from os import environ

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import json

app = Flask(__name__)
CORS(app)

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "totalysmu@gmail.com"
app.config['MAIL_PASSWORD'] = "Totaly@2021"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/notification', methods=['POST'])
def send_message():
    if request.method == 'POST':
        try:
            notification_info = request.get_json()
            print(notification_info)

            emailToSend = notification_info['email']
            withdraw_amount = notification_info['withdraw']
            wallet_balance = notification_info['wallet_balance']
            subject = "Success Redemption from EatBefore"
            msg = "Dear Customer, \n\n Thank you for using EatBefore. You have successfully withdrawn $" + withdraw_amount + ". Your current balance in your wallet is $" + wallet_balance +". \n\n Have a great day ahead! \n \n Regards, \n EatBefore"

            message = Message(subject, sender="totalysmu@gmail.com", recipients=[emailToSend] )

            message.body = msg

            mail.send(message)

            # logging to log microservice
            isOK = log_template.create_log(
                "notification",
                0,
                'create',
                'notification',
                'Successful sending of email to ' + emailToSend + ' at notification microservice. ',
                'success')

            return jsonify({
                "code": 200,
                "message": "Message sent"
            }), 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            # logging to log microservice
            isOK = log_template.create_log(
                "notification",
                0,
                'create',
                'notification',
                'Failure to send notification: \n' + str(e),
                'error')
            
            return jsonify({
                "code": 500,
                "message": "Notification.py internal error: " + str(e)
            }), 500

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "Notification.py is callable!"
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)