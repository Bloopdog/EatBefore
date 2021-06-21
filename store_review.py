#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import datetime

import json

import os, sys
from os import environ

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import log_template

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

upload_URL = environ.get('upload_URL') or "http://localhost:5102/upload"
review_URL = environ.get('review_URL') or "http://localhost:5001/review"

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "Store_review.py is callable!"
        }
    ), 200

# User submits review. Review to be stored in database
@app.route("/storereview", methods=['POST']) # Required Input: All 
def storereview():
    # code
    if request.is_json:
        try:
            review_data = request.get_json()

            last_id = getlastid()
            new_id = last_id + 1
            print("New Review id returned:", new_id)

            # logging to log microservice
            isOK = log_template.create_log(
                "store_review",
                review_data['user_id'],
                'view',
                'review',
                'Successful retrieval of the latest review ID from review microservice to store_review microservice',
                'success')
            
            # extract base64 image and call uploadbase64 function to get image url
            base64str = review_data["imageurl"]
            image_url_returned =  uploadbase64(base64str, new_id)

            # logging to log microservice
            isOK = log_template.create_log(
                "store_review",
                review_data['user_id'],
                'create',
                'image',
                'Successful storage of review ' + str(new_id) + "'s image into s3 at store_review microservice, url for this new image is: " + image_url_returned ,
                'success')
            
            print("Image is returned:",image_url_returned)
            # manipulate main json to replace base64image to returned image URL
            review_data["imageurl"] = image_url_returned
            
            print("New JSON returned:", review_data)
            
            # log review in database
            response_obj = logreview(review_data)
            return jsonify(response_obj), response_obj['code'] 

        except Exception as e:
            
            # logging to log microservice
            isOK = log_template.create_log(
                "store_review",
                0,
                'create',
                'review',
                'Failed storage of review: \n' + str(e),
                'error')
            
            return jsonify({
                "code": 500,
                "message": "Store_Review.py internal error: " + str(e)
            }), 500
    
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def getlastid(): # 1) Get last id

    print('\n-----Invoking review microservice-----')
    review_URL_append = review_URL + '/lastid'
    last_id_json = invoke_http(review_URL_append, method='GET')
    print('Json from review microservive is:\n', last_id_json)
    last_id = last_id_json["data"]["review"]["review_id"]
    return last_id

def uploadbase64(base64str, new_id): # 2) Convert and Upload base64 image to S3

    print('\n-----Invoking upload microservice-----')
    base64json = {
        'new_id': new_id,
        'base64': base64str
    }
    # print(base64json)
    image_URL_json = invoke_http(upload_URL, json=base64json, method='POST')
    image_URL = image_URL_json["url"]

    return image_URL

def logreview(review_data): # 3) Create transaction log for withdrawal

    print('\n-----Invoking review microservice-----')
    review_result = invoke_http(review_URL,json=review_data, method='POST')
    print('review_result:', review_result)

    # logging to log microservice
    isOK = log_template.create_log(
        "store_review",
        review_data['user_id'],
        'create',
        'review',
        'Successful creation of new review at review microservice, called by store_review microservice. Json Response from review microservice:\n' + json.dumps(review_result),
        'success')
    
    return review_result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5203, debug=False)
