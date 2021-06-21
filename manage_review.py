#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import datetime

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

review_URL = environ.get('review_URL') or "http://localhost:5001/review"
user_URL = environ.get('user_URL') or "http://localhost:5002/user"

@app.route("/view_review/<int:review_id>", methods=['GET'])
def view_review(review_id):

    if review_id != None:
        try:
            print("\nReceived review id:", review_id)

            # do the actual work
            # 1. Send review id info 
            result = processReviewWallet(review_id)

            #Should return review information
            print('\n------------------------')
            print('\Returning the following JSON code: ', result)

            # logging to log microservice
            isOK = log_template.create_log(
                "manage_review",
                0,
                'view',
                'review',
                'Successful viewing of review at manage_review microservice.',
                'success')
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            print(str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            # logging to log microservice
            isOK = log_template.create_log(
                "manage_review",
                0,
                'view',
                'review',
                'Failed viewing of review at manage_review microservice.' + str(e),
                'error')

            return jsonify({
                "code": 500,
                "message": "manage_review.py internal error: " + ex_str
            }), 500

    else:
        # logging to log microservice
        isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Failed viewing of review at manage_review microservice. Invalid review id ' + str(review_id)  ,
            'error')

        return jsonify({
            "code": 400,
            "message": "Invalid review id: " + str(review_id)
        }), 400

def processReviewWallet(review_id):
    
    print('\n-----Invoking review microservice-----')
    review_result = invoke_http(review_URL +"/"+str(review_id), method='GET')
    print('review_result:', review_result)
  
    print('\n-----Update view count-----')
    views_result = invoke_http(
            review_URL+"/views/"+str(review_id), method="PUT")
    print("views_result:", views_result, '\n')

    # logging to log microservice
    isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Successful calling of review' + '/' + str(review_id) + ' at manage_review microservice. Returned result is \n' + json.dumps(review_result)  ,
            'success')

    # Check the review result; if a failure, send it to the error microservice.
    code = review_result["code"]
    message = json.dumps(review_result)

    if code not in range(200, 300):
        # logging to log microservice
        isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Failed viewing of review at manage_review microservice. review microservice did not respond with code 200' ,
            'error')
        
        return {
            "code": 500,
            "data": {"review_result": review_result},
            "message": "Failed to get Review information, failure sent for error handling."
        }

    #get review data
    reviewWalletData = review_result['data']
    userID = review_result['data']['review']['user_id']

    user_view_result = invoke_http(user_URL+"/"+str(userID), method="GET")

    # logging to log microservice
    isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Successful calling of user' + '/' + str(userID) + ' at manage_review microservice. Returned result is \n' + json.dumps(user_view_result)  ,
            'success')
    
    userTotalView = user_view_result['data']['total_views']
    print("this is the total view: ", userTotalView)
    
    #If every hundredth view, credit new wallet value to user  
    if (userTotalView+1)%100 == 0:
        #Credit 2 dollars to owner of the review
        reviewWalletData['review']["wallet_balance"]= 2

        print("------JSON that is passed to user/waller/update------")
        print(reviewWalletData)

        #Invoke
        user_result = invoke_http(user_URL+"/wallet/update", method="PUT", json=reviewWalletData)
        
        # logging to log microservice
        isOK = log_template.create_log(
                "manage_review",
                0,
                'view',
                'review',
                'Successful calling of user/wallet/update at manage_review microservice. Returned result is \n' + json.dumps(user_result)  ,
                'success')

        print("Json response from user microservice: \n", user_result, '\n')

    
    else: 
        #If view count is not 100, just update user view count without adding wallet balance
        user_result = invoke_http(user_URL+"/review/view/update", method="PUT", json=reviewWalletData)

        # logging to log microservice
        isOK = log_template.create_log(
                "manage_review",
                0,
                'view',
                'review',
                'Successful calling of user/wallet/update at manage_review microservice. Returned result is \n' + json.dumps(user_result)  ,
                'success')

    # Check the user result;
    # if a failure, send it to the error microservice.
    code = user_result["code"]

    if code not in range(200, 300):
        message = json.dumps(user_result)
        
        # logging to log microservice
        isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Failed viewing of review at manage_review microservice. review microservice did not respond with code 200, this is the json returned ' + message ,
            'error')
        
        # 7. Return error
        return {
            "code": 400,
            "data": {
                "review_result": review_result,
                "user_result": user_result
            },
            "message": "Simulated updating user record, error sent for error handling."
        }

    # 7. Return created review information
    if userTotalView%100 == 0:
        del review_result['data']['review']['wallet_balance']
    
    # logging to log microservice
    isOK = log_template.create_log(
            "manage_review",
            0,
            'view',
            'review',
            'Successful viewing of review at manage_review microservice. Now returning created review info to caller',
            'success')
    return {
        "code": 200,
        "data": review_result['data']
        
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5201, debug=False)