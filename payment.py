#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json

import os, sys
from os import environ

import log_template

#Serves as a wrapper to Paypal External Services
from flask import Flask, request, jsonify
from flask_cors import CORS

import datetime

from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError

app = Flask(__name__)
CORS(app)

# Creating Access Token for Sandbox
client_id = "AaraIBH5te0PC2oAM1w-kjHJmXYZ5bze-jaF5__oN5DN_fP_m80WzKKKqqOXfaDS681WKVR95HGqOABi"
client_secret = "EPPczJKIbOOPl6wQejTRgUo-gd1Wu_GnxYkouDyebDzpdSTrzYGT9PXIY1pkHKChiKxKzvunv89sekwc"
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

# Batch Payout

# Construct a request object and set desired parameters
# Here, PayoutsPostRequest() creates a POST request to /v1/payments/payouts

#Payment Call
@app.route("/payment", methods=["POST"])
def pay_from_paypal():
    data = request.get_json()
    withdraw_amount = data["withdraw_amount"]
    email = data["email"]
    time = datetime.datetime.now()

    batch_id = email + str(time)

    print("following details: ", batch_id , " type:", type(batch_id), " email:", email, " type:", type(email))
    body = {
        "sender_batch_header": {
            "recipient_type": "EMAIL",
            "email_message": "Food Review Payout",
            "note": "Thank you for contributing to our wonderful community!!",
            "sender_batch_id": f"{batch_id}",
            "email_subject": f"Payout from Eatbefore {batch_id}"
        },
        "items": [{
            "note": f"Your SGD${withdraw_amount} Payout!",
            "amount": {
                "currency": "SGD",
                "value": f"{withdraw_amount}"
            },
            "receiver": email,
            "sender_item_id": f"{batch_id}"
        }]
    }
    print("body here: ")
    print (body)
    requestPaypal = PayoutsPostRequest()
    requestPaypal.request_body(body)

    try:
        # Call API with your client and get a response for your call
        response = client.execute(requestPaypal)

        # logging to log microservice
        isOK = log_template.create_log(
            "payment",
            0,
            'create',
            'payment',
            'Successful payment of ' + str(withdraw_amount) + ' to email ' + email + ' at payment microservice.',
            'success')
        
        # If call returns body in response, you can get the deserialized version from the result attribute of the response
        batch_id = response.result.batch_header.payout_batch_id
        print ("Response Here: ", response.result)  
        return jsonify(
            {
                "code": 200,
                "result": "Payment is successful"
            }   
        )
            
    except IOError as ioe:
        print (ioe)
        if isinstance(ioe, HttpError):
           
            # logging to log microservice
            isOK = log_template.create_log(
                "payment",
                0,
                'create',
                'payment',
                'Failed payment at payment microservice. Something went wrong at Payment with Paypal. ' + str(ioe),
                'error')

            return jsonify(
            {
                "code": 500,
                "message": "An error occurred while processing payment. " + str(ioe) 
            }   
            )
    # logging to log microservice
    isOK = log_template.create_log(
        "payment",
        0,
        'create',
        'payment',
        'Failed payment at payment microservice.' ,
        'error')
    return jsonify(
        {
            "code": 400,
            "message":"An error occurred while processing payment"
        }
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5101, debug=False)