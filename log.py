#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

# Database for logging should be like
# ID, source, user, action, data, description, status
# INSERT INTO `log` (`user`, `action`, `data`, `description`, `status`, `log_timestamp`) 

# Sample data
# VALUES (NULL, "create", "user", 'Successfully created user Orange LEE', 'success','2021-01-11 02:14:57');

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

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213:totaly2021@34.87.173.70:3306/log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Log(db.Model):
    __tablename__ = 'log'

    log_id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    microservice = db.Column(db.String(32), nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(32), nullable=False)
    data = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(16), nullable=False)
    log_timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, microservice, userid, action, data, description, status, log_timestamp):
        self.microservice = microservice
        self.userid = userid
        self.action = action
        self.data = data
        self.description = description
        self.status = status
        self.log_timestamp = log_timestamp

    def json(self):
        return {
            "log_id": self.log_id,
            "microservice": self.microservice,
            "userid": self.userid,
            "action": self.action,
            "data": self.data,
            "description": self.description,
            "status": self.status,
            "log_timestamp": self.log_timestamp,
        }

monitorBindingKey='#'

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "log.py is callable!"
        }
    )

@app.route("/log/create", methods=["POST"])
def create_log():
    data = request.get_json()
    log = Log(**data)

    try:
        db.session.add(log)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the log."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": log.json()
        }
    ), 500

@app.route("/log", methods=["GET"])
def get_all_logs():
    loglist = Log.query.all()
    if len(loglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [log.json() for log in loglist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no logs."
        }
    ), 404

def receivelog():
    amqp_setup.check_setup()
        
    queue_name = 'log'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(json_log):
    print("Recording a log:")
    print(json_log)
    log_to_db(json_log)

def log_to_db(data):
    log = Log(**data)

    try:
        db.session.add(log)
        db.session.commit()
        print("Successfully created log into db")
    except Exception as e:

        print("Error with storing log data into log db", str(e))

    return 

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receivelog()
    app.run(host='0.0.0.0', port=5005, debug=False)

