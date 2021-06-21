#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json

import os, sys
from os import environ

from flask import Flask, request, jsonify
from flask_cors import CORS

import log_template

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

payment_URL = environ.get('payment_URL') or "http://localhost:5101/payment"
user_URL = environ.get('user_URL') or "http://localhost:5002/user"
transaction_URL = environ.get('transaction_URL') or "http://localhost:5003/transaction"
notification_URL = environ.get('notification_URL') or "http://localhost:5004"

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "Redemption.py is callable!"
        }
    ), 200

# User withdraw money from their wallet
@app.route("/redemption", methods=['POST']) # Required Input: user_id, withdraw_amount, email address
def redemption():

    if request.is_json: # Simple check of input format and data of the request are JSON

        try:
            redemption_info = request.get_json() # retrieve in dict data type
            print("\nReceived redemption information in JSON:", redemption_info)

            # retrieve inputs
            user_id = str(redemption_info["user_id"])
            withdraw_amount = redemption_info["amount"]
            email = redemption_info["email"]

            wallet_balance = check_wallet(user_id) # Get wallet balance of given user to check legitability
            
            if wallet_balance["code"] == 200: # Check calling of wallet balance is successful

                # Check if wallet balance more than withdraw amount
                if wallet_balance["data"]["wallet_balance"] < withdraw_amount: 
                    # logging to log microservice
                    isOK = log_template.create_log(
                        "redemption",
                        int(user_id),
                        'update',
                        'user',
                        'Failed withdrawl of ' + str(withdraw_amount) + ' for user ' + str(user_id) + ' at redemption microservice, withdrawl amount higher than wallet balance',
                        'error')

                    return jsonify({
                        "code": 400,
                        "message": "Unable to withdraw. Withdrawal amount higher than wallet balance!"
                    }), 400
                else:    
                    # Assume deduction from wallet is successful
                    # Proceed to call transaction microservice to create transaction log
                    wallet_balance["data"]["withdraw_amount"] = withdraw_amount
                    payment_details = wallet_balance["data"]

                    #Invoke Payment Wrapper Service
                    payment_result = invoke_http(payment_URL, method="POST", json=payment_details)
                    print("payment_result:", payment_result, '\n')

                    # logging to log microservice
                    isOK = log_template.create_log(
                        "redemption",
                        0,
                        'create',
                        'payment',
                        'Successful invoking of ' + payment_URL + ' at redemption microservice to pay user.\n This is the sent JSON:' + json.dumps(payment_details) + ' \nThis is the received json: \n' + json.dumps(payment_result),
                        'success')

                    if payment_result["code"] not in range(200, 300):
                        # logging to log microservice
                        isOK = log_template.create_log(
                            "redemption",
                            0,
                            'create',
                            'payment',
                            'Error after invoking of ' + payment_URL + ' at redemption microservice to pay user.\n This is the sent JSON:' + json.dumps(payment_details) + ' \nThis is the received json: \n' + json.dumps(payment_result),
                            'error')
                    
                        return payment_result
                    
                    
                    # Required Input: user_id, transaction_type, transaction_amount
                    data = {
                        "user_id": int(user_id),
                        "transaction_type": "withdraw",
                        "transaction_amount": withdraw_amount
                    }

                    transaction_results = transaction_result(data) # Log withdrawal transaction

                    if transaction_results["code"] not in range(200, 300):
                        # logging to log microservice
                        isOK = log_template.create_log(
                            "redemption",
                            0,
                            'create',
                            'transaction',
                            'Error after invoking of transaction microservice at redemption microservice to create new transaction entry.\nThis is the received json: \n' + json.dumps(transaction_results),
                            'error')
                        return transaction_results
                    
                    
                    # Update wallet balance on user.py
                    wallet_balance = wallet_balance["data"]["wallet_balance"] - withdraw_amount

                    # Required Input: user_id, wallet_balance
                    data = {
                        "user_id": int(user_id),
                        "wallet_balance": str(wallet_balance)
                    }
                    update_wallet_result = update_wallet(data) # Update wallet data

                    if update_wallet_result["code"] in range(200, 300):
                        notification_data = {
                            "email": email,
                            "withdraw": str(withdraw_amount),
                            "wallet_balance": str(wallet_balance)
                        }
                        notify_user(notification_data) # Send email to notify users that they are 
                    
                    # logging to log microservice
                    isOK = log_template.create_log(
                        "redemption",
                        0,
                        'create',
                        'payment',
                        'Successful overall redemption of funds from wallet at redemption microservice.\nThis is the returned json: \n' + json.dumps(update_wallet_result),
                        'success')
                    return update_wallet_result # Return success code and message

            # If there's error on getting wallet balance
            # logging to log microservice
            isOK = log_template.create_log(
                "redemption",
                0,
                'create',
                'payment',
                'Failed overall redemption of funds from wallet at redemption microservice.',
                'error')
            return wallet_balance
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)
            
            # logging to log microservice
            isOK = log_template.create_log(
                "redemption",
                0,
                'create',
                'payment',
                'Failed overall redemption of funds from wallet at redemption microservice.\nThis is the error: \n' + str(e),
                'error')
            
            return jsonify({
                "code": 500,
                "message": "Redemption.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def check_wallet(user_id): # 1) Check wallet balance to ensure legitability
    
    print('\n-----Invoking user microservice-----')
    user_URL_append = user_URL + '/' + str(user_id) + "/wallet"
    user_wallet_balance = invoke_http(user_URL_append, method='GET')

    # logging to log microservice
    isOK = log_template.create_log(
        "redemption",
        user_id,
        'view',
        'user',
        'Successful invoking of ' + user_URL + '/' + str(user_id) + "/wallet" + ' at redemption microservice. This is the received json: \n' + json.dumps(user_wallet_balance),
        'success')
    
    print('user_wallet_balance:', user_wallet_balance)
    return user_wallet_balance

def transaction_result(transaction_data): # 2) Create transaction log for withdrawal
    
    print('\n-----Invoking transaction microservice-----')
    transaction_URL_append =  transaction_URL + "/create"
    transaction_result = invoke_http(transaction_URL_append,json=transaction_data, method='POST')

    # logging to log microservice
    isOK = log_template.create_log(
        "redemption",
        0,
        'create',
        'transaction',
        'Successful invoking of ' + transaction_URL + "/create" + ' at redemption microservice. This is the received json: \n' + json.dumps(transaction_result),
        'success')
    
    print('transaction_result:', transaction_result)
    return transaction_result

def update_wallet(data): # 3) Update user wallet after withdrawal
    print('\n-----Invoking user microservice-----')
    user_URL_append =  user_URL + "/wallet"
    update_wallet_result = invoke_http(user_URL_append, json=data, method='PUT')

    # logging to log microservice
    isOK = log_template.create_log(
        "redemption",
        0,
        'update',
        'user',
        'Successful invoking of ' + user_URL + "/wallet" + ' at redemption microservice to update user wallet balance. This is the received json: \n' + json.dumps(update_wallet_result),
        'success')
    
    print('update_wallet_result:', update_wallet_result)
    return update_wallet_result

def notify_user(emailjson): # 4) Notify user email
    print('\n-----Invoking notification microservice-----')
    notification_URL_append =  notification_URL + "/notification"
    notification_result = invoke_http(notification_URL_append, json=emailjson, method='POST')

    # logging to log microservice
    isOK = log_template.create_log(
        "redemption",
        0,
        'create',
        'notification',
        'Successful invoking of ' + notification_URL + "/notification" + ' at redemption microservice to notify user via email. This is the received json: \n' + json.dumps(notification_result),
        'success')
    
    print('notification_result:', notification_result)
    return notification_result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5202, debug=False)