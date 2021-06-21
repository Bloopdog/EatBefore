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

from sqlalchemy import desc

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213:totaly2021@34.87.173.70:3306/review'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Review(db.Model):
    __tablename__ = 'review'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    place_id = db.Column(db.String(255), nullable=False)
    place_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_title = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.String(5000), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    imageurl = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, user_name, place_id, place_name, rating, review_title, review_text, likes, views, imageurl):
        self.user_id = user_id
        self.user_name = user_name
        self.place_id = place_id
        self.place_name = place_name
        self.rating = rating
        self.review_title = review_title
        self.review_text = review_text
        self.likes = likes
        self.views = views
        self.imageurl = imageurl
        self.created = log_template.get_curr_time()
        self.modified = log_template.get_curr_time()

    def json(self):
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "place_id": self.place_id,
            "place_name": self.place_name,
            "rating": self.rating,
            "review_title": self.review_title,
            "review_text": self.review_text,
            "likes": self.likes,
            "views": self.views,
            "imageurl": self.imageurl,
            "created": self.created,
            "modified": self.modified
        }

class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    review_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(32), nullable=False)
    comment_text = db.Column(db.String(500), nullable=False)
    comment_likes = db.Column(db.Integer, nullable=False)
    comment_created = db.Column(db.DateTime, nullable=False)
    comment_modified = db.Column(db.DateTime, nullable=False)

    def __init__(self, review_id, user_id, user_name, comment_text, comment_likes):
        self.review_id = review_id
        self.user_id = user_id
        self.user_name = user_name
        self.comment_text = comment_text
        self.comment_likes = comment_likes
        self.comment_created = log_template.get_curr_time()
        self.comment_modified = log_template.get_curr_time()

    def json(self):
        return {
            "comment_id": self.comment_id,
            "review_id": self.review_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "comment_text": self.comment_text,
            "comment_likes": self.comment_likes,
            "comment_created": self.comment_created,
            "comment_modified": self.comment_modified
        }

# Test if the python file is running and callable
@app.route("/testpoint")
def testpoint():
    return jsonify(
        {
            "code": 200,
            "message": "Review.py is callable!"
        }
    )

# get all reviews
@app.route("/review")
def get_all():
    try :
        reviewlist = Review.query.all()
        if len(reviewlist):

            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of all reviews at review microservice',
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reviews": [review.json() for review in reviewlist]
                    }
                }
            )
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of all reviews at review microservice, there are no reviews',
            'error')

        return jsonify(
            {
                "code": 404,
                "message": "There are no reviews."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of all reviews at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving all reviews. " + str(e)
            }
        )

# get all reviews in sorted ratings order
@app.route("/review/sorted/rating")
def sort_by_rating():
    try:
        reviewlist = Review.query.order_by(desc("rating")).all()
        if len(reviewlist):
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of sorted rating reviews at review microservice.',
                'success')
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reviews": [review.json() for review in reviewlist]
                    }
                }
            )
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of sorted rating reviews at review microservice, there are no reviews',
            'error')
        return jsonify(
            {
                "code": 404,
                "message": "There are no reviews."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of sorted rating reviews at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving sorted rating reviews. " + str(e)
            }
        )

# get all reviews in sorted order
@app.route("/review/sorted/views")
def sort_by_views():
    try:
        reviewlist = Review.query.order_by(desc("views")).all()
        if len(reviewlist):
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of view sorted reviews at review microservice.',
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reviews": [review.json() for review in reviewlist]
                    }
                }
            )
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of view-sorted reviews at review microservice, there are no reviews',
            'error')
        return jsonify(
            {
                "code": 404,
                "message": "There are no reviews."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of view-sorted reviews at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving view-sorted reviews. " + str(e)
            }
        )


# get last review in sorted review_id desc order
@app.route("/review/lastid")
def sort_by_desc_id():
    try:
        reviewlist = Review.query.order_by(desc("review_id")).all()
        print(reviewlist)
        if len(reviewlist):
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of sorted rating reviews at review microservice.',
                'success')
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "review": reviewlist[0].json()
                    }
                }
            ), 200
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of sorted rating reviews at review microservice, there are no reviews',
            'error')
        return jsonify(
            {
                "code": 404,
                "message": "There are no reviews."
            }
        ), 404
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of sorted rating reviews at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving last review id review. " + str(e)
            }
        ), 500

# retrieve a review
@app.route("/review/<int:review_id>")
def find_by_review(review_id):
    try:
        review = Review.query.filter_by(review_id=review_id).first()
        if review:
            comments = Comment.query.filter_by(review_id=review_id)
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of review' + str(review_id) + ' at review microservice.',
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "review": review.json(),
                        "comments": [comment.json() for comment in comments]
                    }
                }
            )
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of review ' + str(review_id) + ' at review microservice, review not found.',
            'error')
        
        return jsonify(
            {
                "code": 404,
                "message": "Review not found."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of review' + str(review_id) + ' at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving review " + str(review_id) + ' , '+ str(e)
            }
        )

# retrieve all reviews of a place
@app.route("/review/<string:place_name>")
def find_by_place(place_name):
    try:
        storeReviews = Review.query.filter_by(place_name=place_name)
        if storeReviews:
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                0,
                'view',
                'review',
                'Successful viewing of reviews for location ' + place_name + ' at review microservice.',
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reviews": [review.json() for review in storeReviews]
                    }
                }
            )
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of reviews at location ' + place_name + ' at review microservice, no reviews found.',
            'error')

        return jsonify(
            {
                "code": 404,
                "message": "No reviews found."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'view',
            'review',
            'Failed viewing of review at location' + place_name + ' at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving review for " + place_name + ' , '+ str(e)
            }
        )


# retrieve all reviews made by a user
@app.route("/review/user/<int:user_id>")
def find_by_user(user_id):
    try:
        userReviews = Review.query.filter_by(user_id=user_id)
        if userReviews:
            # logging to log microservice
            isOK = log_template.create_log(
                "review",
                user_id,
                'view',
                'review',
                'Successful viewing of reviews by userid ' + str(user_id) + ' at review microservice.',
                'success')
            
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "reviews": [review.json() for review in userReviews]
                    }
                }
            )
        
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            user_id,
            'view',
            'review',
            'Failed viewing of reviews by userid ' + str(user_id) + ' at review microservice, no reviews found.',
            'error')
        
        return jsonify(
            {
                "code": 404,
                "message": "No reviews found."
            }
        )
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            user_id,
            'view',
            'review',
            'Failed viewing of reviews by userid' + str(user_id) + ' at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "There was an issue retrieving reviews by user " + str(user_id) + ' , '+ str(e)
            }
        )

# create a review
@app.route("/review", methods=["POST"])
def create_review():
    try:
        data = request.get_json()
        review = Review(**data)

        user_id = data['user_id']
        review_title = data['review_title']

        db.session.add(review)
        db.session.commit()
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'create',
            'review',
            'Failed creation of review at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the review. " + str(e)
            }
        ), 500
    
    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        user_id,
        'create',
        'review',
        'Successful creation of review titled ' + review_title + ' by userid ' + str(user_id) + ' at review microservice.',
        'success')
    return jsonify(
        {
            "code": 201,
            "data": review.json()
        }
    ), 201


# create a comment
@app.route("/review/comment", methods=["POST"])
def create_comment():
    try:
        data = request.get_json()
        comment = Comment(**data)
        user_id = data['user_id']

        db.session.add(comment)
        db.session.commit()

    except Exception as e:
        error_msg = "An error occurred creating the comment, " + str(e) 

        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'create',
            'comment',
            'Failed creation of comment at review microservice, ' + str(e),
            'error')
        
        return jsonify(
            {
                "code": 500,
                "message": error_msg
            }
        ), 500

    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        user_id,
        'create',
        'comment',
        'Successful creation of comment by userid ' + str(user_id) + ' at review microservice.',
        'success')

    return jsonify(
        {
            "code": 201,
            "data": comment.json()
        }
    ), 201

# update views count
@app.route("/review/views/<int:review_id>", methods=["PUT"])
def update_view(review_id):
    try:
        review = Review.query.filter_by(review_id=review_id).first()    
        review.views = review.views + 1
        db.session.commit()

    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'update',
            'review',
            'Failed update of view count at review microservice, ' + str(e),
            'error')

        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the view count, " + str(e)
            }
        ), 500
    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        0,
        'update',
        'review',
        'Successful update of view count for review id ' + str(review_id) + ' at review microservice.',
        'success')
    return jsonify(
        {
            "code": 200,
            "data": review.json()
        }
    ), 200

# update likes count
@app.route("/review/likes/<int:review_id>", methods=["PUT"])
def update_likes(review_id):
    try:
        review = Review.query.filter_by(review_id=review_id).first()    
        review.likes = review.likes + 1
        db.session.commit()

    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'update',
            'review',
            'Failed update of number of likes at review microservice, ' + str(e),
            'error')

        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the number of likes, " + str(e)
            }
        ), 500
    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        0,
        'update',
        'review',
        'Successful update of number of likes for review id ' + str(review_id) + ' at review microservice.',
        'success')
    return jsonify(
        {
            "code": 200,
            "data": review.json()
        }
    ), 200

# update a review
@app.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    data = request.get_json()
    rating = data["rating"]
    review_title = data["review_title"]
    review_text = data["review_text"]
    review = Review.query.filter_by(review_id=review_id).first()

    print(data)
    try:
        review.rating = rating
        review.review_title = review_title
        review.review_text = review_text
        review.modified = log_template.get_curr_time()
        db.session.commit()
    except Exception as e:
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'update',
            'review',
            'Failed update of review at review microservice, ' + str(e),
            'error')
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the review, " + str(e)
            }
        ), 500

    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        0,
        'update',
        'review',
        'Successful update of review for review id ' + str(review_id) + ' at review microservice.',
        'success')
    print(review.json())
    return jsonify(
        {
            "code": 200,
            "data": review.json()
        }
    ), 200

# delete a review
@app.route("/review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = Review.query.filter_by(review_id=review_id).first()
    try:
        db.session.delete(review)
        db.session.commit()
    except Exception as e:
        print(str(e))
        # logging to log microservice
        isOK = log_template.create_log(
            "review",
            0,
            'delete',
            'review',
            'Failed delete of review at review microservice. ' + str(e),
            'error')
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred deleting the review, " + str(e)
            }
        ), 500
    
    # logging to log microservice
    isOK = log_template.create_log(
        "review",
        0,
        'delete',
        'review',
        'Successful delete of review for review id ' + str(review_id) + ' at review microservice.',
        'success')
    
    print('returning the following json: \n', review.json())
    return jsonify(
        {
            "code": 200,
            "data": {
                "review_id": review_id
            }
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)