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
from invokes import invoke_http

from botocore.vendored import requests
import requests
import base64
import boto3
import boto

app = Flask(__name__)
CORS(app)

# Upload image to S3 -> Input base64, Output {"url": Url stored in S3} JSON
@app.route("/upload", methods=['POST']) # Required Input: base64
def upload():
    try:
        if request.is_json: # Simple check of input format and data of the request are JSON
            upload_info = request.get_json() # retrieve in dict data type
            print("\nReceived upload information in JSON:", upload_info)
            print("type upload info", type(upload_info))
            
            #where the file will be uploaded, if you want to upload the file to folder use 'Folder Name/FileName.jpeg'
            s3 = boto3.resource('s3', aws_access_key_id="AKIAYV4ODAN2IAJA4SHZ", aws_secret_access_key="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")

            new_id = upload_info["new_id"]
            url_to_download = upload_info["base64"]
            file_name_with_extension = "r/" + str(new_id) + '.jpg'
            
            print("url to download", url_to_download)

            def lambda_handler():
                # image_base64 = get_as_base64(url_to_download)
                image_base64 = url_to_download
                print(image_base64)
                obj = s3.Object("esd-image",file_name_with_extension)
                obj.put(Body=base64.b64decode(image_base64))

                #get object url
                object_url = "https://%s.s3.amazonaws.com/%s" % ("esd-image",file_name_with_extension)
                print("Success:", object_url)

                # logging to log microservice
                isOK = log_template.create_log(
                    "upload",
                    0,
                    'create',
                    'image',
                    'Successful creation of image at s3 with filepath ' + object_url + ' at upload microservice.',
                    'success')
                
                return json.dumps({"code": 201,"url":object_url}),201

            return lambda_handler()
    
    except Exception as e:
        
        # logging to log microservice
        isOK = log_template.create_log(
            "upload",
            0,
            'create',
            'image',
            'Failed creation of image at s3 at upload microservice.',
            'error')
        
        error_json = {
            "code":500,
            "message": "Something went wrong with storing image at s3, " + str(e)
        }

        return json.dumps(error_json),500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5102, debug=False)


