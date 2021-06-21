#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

# Database for errors should be like
# ID, source, user, action, data, description, status
# INSERT INTO `log` (`user`, `action`, `data`, `description`, `status`, `log_timestamp`) 

# Sample data
# VALUES ("user", 1, "view", "user", "Failed viewing of user 1's wallet balance at user microservice, User not found", "error", '2020-06-12 02:14:58');


import datetime

import json

import os
from os import environ

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import amqp_setup

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213:totaly2021@34.87.173.70:3306/error'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Error(db.Model):
    __tablename__ = 'error'

    error_id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    microservice = db.Column(db.String(32), nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(32), nullable=False)
    data = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(16), nullable=False)
    error_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, microservice, userid, action, data, description, status, error_timestamp):
        self.microservice = microservice
        self.userid = userid
        self.action = action
        self.data = data
        self.description = description
        self.status = status
        self.error_timestamp = error_timestamp

    def json(self):
        return {
            "error_id": self.error_id,
            "microservice": self.microservice,
            "userid": self.userid,
            "action": self.action,
            "data": self.data,
            "description": self.description,
            "status": self.status,
            "error_timestamp": self.error_timestamp,
        }

monitorBindingKey='error.#'

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "error.py is callable!"
        }
    )

@app.route("/error/create", methods=["POST"])
def create_error():
    data = request.get_json()
    error = Error(**data)

    try:
        db.session.add(error)
        db.session.commit()
    except Exception as e:
        err_message = "An error occurred creating the error log, " + str(e)
        
        return jsonify(
            {
                "code": 500,
                "message": err_message
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": error.json()
        }
    ), 500

@app.route("/error", methods=["GET"])
def get_all_errors():
    error_list = Error.query.all()
    if len(error_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [error.json() for error in error_list]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no error logs."
        }
    ), 404

def receive_error():
    amqp_setup.check_setup()
        
    queue_name = 'error'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error log by " + __file__)
    processErrorLog(json.loads(body))
    print() # print a new line feed

def processErrorLog(json_error):
    print("Recording an error log:")
    json_error['error_timestamp'] = json_error['log_timestamp']
    json_error.pop('log_timestamp')
    print(json_error)
    error_to_db(json_error)

def error_to_db(data):
    error = Error(**data)

    try:
        db.session.add(error)
        db.session.commit()
        print("Successfully created error log into db")
    except Exception as e:
        print("Error with storing error log data into error db" + str(e))

    return 

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receive_error()
    app.run(host='0.0.0.0', port=5006, debug=False)

