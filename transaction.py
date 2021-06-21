#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import datetime

import json

import os
from os import environ

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import log_template

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213:totaly2021@34.87.173.70:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(8), nullable=False)
    transaction_amount = db.Column(db.Float(4), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, transaction_type, transaction_amount):
        transaction_date = datetime.datetime.now()
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.transaction_amount = transaction_amount
        self.transaction_date = log_template.get_curr_time()

    def json(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "transaction_type": self.transaction_type,
            "transaction_amount": self.transaction_amount,
            "transaction_date": self.transaction_date
        }

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "Transaction.py is callable!"
        }
    ), 200

# get all transactions
@app.route("/transaction")
def get_all():
    transactionlist = Transaction.query.all()
    if len(transactionlist):
        # logging to log microservice
        isOK = log_template.create_log(
            "transaction",
            0,
            'view',
            'transaction',
            'Successful viewing of all transactions at transaction microservice',
            'success')
        
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        ), 200
    # logging to log microservice
        isOK = log_template.create_log(
            "transaction",
            0,
            'view',
            'transaction',
            'Failed viewing of all transactions at transaction microservice, there are no transactions',
            'error')
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no transactions."
        }
    ), 404

# retrieve all transactions by a user
@app.route("/transaction/user/<int:user_id>")
def find_by_user(user_id):
    transactionlist = Transaction.query.filter_by(user_id=user_id)
    if transactionlist:
        # logging to log microservice
        isOK = log_template.create_log(
            "transaction",
            user_id,
            'view',
            'transaction',
            'Successful viewing of transactions for user ' + str(user_id) + ' at transaction microservice',
            'success')
        
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        ), 200
    # logging to log microservice
    isOK = log_template.create_log(
        "transaction",
        user_id,
        'view',
        'transaction',
        'Failed viewing of all transactions for user ' + str(user_id) + ' at transaction microservice, there are no transactions',
        'error')
    
    return jsonify(
        {
            "code": 404,
            "message": "There are no transactions."
        }
    ), 404

# retrieve a transaction
@app.route("/transaction/<int:transaction_id>")
def find_by_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if transaction:
        # logging to log microservice
        isOK = log_template.create_log(
            "transaction",
            0,
            'view',
            'transaction',
            'Successful viewing of transaction id ' + str(transaction_id) + ' at transaction microservice',
            'success')
        
        return jsonify(
            {
                "code": 200,
                "message": transaction.json()
            }
        )
    # logging to log microservice
    isOK = log_template.create_log(
        "transaction",
        0,
        'view',
        'transaction',
        'Failed viewing of transaction id ' + str(transaction_id) + ' at transaction microservice, transaction not found',
        'error')
    
    return jsonify(
        {
            "code": 404,
            "message": "Transaction not found"
        }
    ), 404

# create a transaction
@app.route("/transaction/create", methods=["POST"])
def create_transaction():
    data = request.get_json()
    transaction = Transaction(**data)

    try:
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "transaction",
            0,
            'view',
            'transaction',
            'Failed creation of transaction at transaction microservice, ' + str(e),
            'error')
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the transaction." + str(e)
            }
        ), 500
    # logging to log microservice
    isOK = log_template.create_log(
        "transaction",
        0,
        'view',
        'transaction',
        'Successful creation of transaction at transaction microservice. ',
        'success')
    return jsonify(
        {
            "code": 201,
            "data": transaction.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)