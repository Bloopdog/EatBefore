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

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213:totaly2021@34.87.173.70:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    user_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    wallet_balance = db.Column(db.Float(10), nullable=False)
    total_views = db.Column(db.Integer, nullable=False)

    def __init__(self, user_name, password, email, wallet_balance, total_views):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.wallet_balance = wallet_balance
        self.total_views = total_views

    def json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "wallet_balance": self.wallet_balance,
            "total_views": self.total_views
        }

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "User.py is callable!"
        }
    ), 200

# retrieve user details
@app.route("/user/<int:user_id>")
def find_by_user(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user_json = user.json()

            # logging to log microservice
            isOK = log_template.create_log(
                "user",
                user_json['user_id'],
                'view',
                'user',
                'Successful viewing of user ' + str(user_json['user_id']) + "'s details at user microservice",
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": user_json
                }
            ), 200

        isOK = log_template.create_log(
                "user",
                user_id,
                'view',
                'user',
                'Failed viewing of user ' + str(user_id) + ' details at user microservice, User not found',
                'error')

        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404
    
    except Exception as e:

        isOK = log_template.create_log(
                "user",
                user_id,
                'view',
                'user',
                'Failed viewing of user ' + str(user_id) + ' details at user microservice, User not found',
                'error')

        return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404

# retrieve wallet value
@app.route("/user/<int:user_id>/wallet", methods=["GET"])
def get_wallet_balance(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if user:

            user_json = user.json()
            isOK = log_template.create_log(
                "user",
                user_json['user_id'],
                'view',
                'user',
                "Successful viewing of user " + str(user_json['user_id']) + "'s wallet balance at user microservice",
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                    "wallet_balance": user.wallet_balance,
                    "email": user.email #Send back email to pay via PayPal
                    }
                }
            ), 200
        
        isOK = log_template.create_log(
                "user",
                user_id,
                'view',
                'user',
                'Failed viewing of user ' + str(user_id) + "'s wallet balance at user microservice, User not found",
                'error')
        
        return jsonify(
            {
                "code": 404,
                "message": "User not found."
            }
        ), 404
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            user_id,
            'view',
            'user',
            'Failed viewing of user ' + str(user_id) + "'s wallet balance at user microservice, " + str(e),
            'error')

        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500

# update user wallet balance after viewing review
@app.route("/user/wallet/update", methods=['PUT'])
def update_wallet_balance():
    try:
        data = request.get_json()
        user_id = data['review']['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        print("this is the user id:" + str(data['review']['user_id']))
        print("this is the wallet balance:" + str(data['review']['wallet_balance']))

        if not user:

            isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s wallet balance at user microservice, User not found",
            'error')

            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "user_id": user_id
                    },
                    "message": "User not found."
                }
            ), 404
        # update status
        if data['review']['wallet_balance']:
            #Current wallet balance plus new wallet balance from json
            user.wallet_balance = user.wallet_balance + data['review']['wallet_balance']
            user.total_views = user.total_views + 1
            db.session.commit()

            isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            "Successful updating of user " + str(user_id) + "'s wallet balance at user microservice",
            'success')

            return jsonify(
                {
                    "code": 200,
                    "data": user.json()
                }
            ), 200
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s wallet balance at user microservice, " + str(e),
            'error')

        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": user_id
                },
                "message": "An error occurred while updating user. " + str(e)
            }
        ), 500


# update user view count after viewing review
@app.route("/user/review/view/update", methods=['PUT'])
def update_view():
    try:
        data = request.get_json()
        user_id = data['review']['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if not user:

            isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s view count at user microservice, User not found",
            'error')

            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "user_id": user_id
                    },
                    "message": "User not found."
                }
            ), 404
        # update status
        user.total_views = user.total_views + 1
        db.session.commit()

        isOK = log_template.create_log(
        "user",
        user_id,
        'update',
        'user',
        "Successful updating of user " + str(user_id) + "'s view count at user microservice",
        'success')

        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        ), 200
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s view count at user microservice, " + str(e),
            'error')

        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": user_id
                },
                "message": "An error occurred while updating user. " + str(e)
            }
        ), 500

# update user wallet after redemption
@app.route("/user/wallet", methods=['PUT']) # Required Input: user_id, wallet_balance
def wallet_balance():
    try:
        data = request.get_json()
        user_id = data['user_id']
        wallet_balance = data['wallet_balance']
        user = User.query.filter_by(user_id=user_id).first()
        if not user:

            isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s wallet balance after redemption at user microservice, User not found",
            'error')

            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404
        if wallet_balance:
            user.wallet_balance = wallet_balance
            db.session.commit()

            isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            "Successful updating of user " + str(user_id) + "'s wallet balance after redemption at user microservice",
            'success')

            return jsonify(
                {
                    "code": 200,
                    "data": user.json()
                }
            ), 200
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            user_id,
            'update',
            'user',
            'Failed updating of user ' + str(user_id) + "'s wallet balance after redemption at user microservice, " + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the wallet balance. " + str(e)
            }
        ), 500

# create a user
@app.route("/user/create", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(**data)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            0,
            'create',
            'user',
            'Failed creation of user ' + str(0) + " at user microservice, " + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": str(e)
            }
        ), 500

    user_json = user.json()

    isOK = log_template.create_log(
            "user",
            user_json['user_id'],
            'create',
            'user',
            "Successful creation of user " + str(user_json['user_id']) + " at user microservice",
            'success')
        
    return jsonify(
        {
            "code": 201, 
            "data": user_json
        }
    ), 201

# validate user login
@app.route("/user/login", methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if not user:

            isOK = log_template.create_log(
                    "user",
                    0,
                    'view',
                    'user',
                    "Failed login of user at user microservice, user with email " + email + ' not found',
                    'warning')
            
            return jsonify(
                {
                    "code": 404,
                    "message": "User not found."
                }
            ), 404
        else:
            if user.email == email and user.password == password:
                user_json = user.json()

                isOK = log_template.create_log(
                    "user",
                    user_json['user_id'],
                    'view',
                    'user',
                    "Successful login of user " + str(user_json['user_id']) + " with email " + email + " at user microservice",
                    'success')

                return jsonify(
                    {
                        "code": 200, 
                        "data": user_json
                    }
                ), 200
            else:

                isOK = log_template.create_log(
                    "user",
                    0,
                    'view',
                    'user',
                    "Failed login of user at user microservice, user with email " + email + ' tried login with incorrect password or email',
                    'warning')
                
                return jsonify(
                    {
                        "code": 404,
                        "message": "Failed to login"
                    }
                ), 404
    except Exception as e:

        isOK = log_template.create_log(
            "user",
            0,
            'view',
            'user',
            "Failed login of user at user microservice, " + str(e),
            'error')

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while trying to login. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
