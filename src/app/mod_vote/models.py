from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

"""This is the model for Upvote class"""
class Upvote(db.Model):
	__tablename__ = "upvotes"
	vote_id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))
	answer_id = db.Column(db.Integer,db.ForeignKey('answers.answer_id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))

	def __repr__(self):
		return '<Upvote %r>' % (self.vote_id)

"""This is the model for Downvote class"""
class Downvote(db.Model):
	__tablename__ = "downvotes"
	vote_id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'))
	answer_id = db.Column(db.Integer,db.ForeignKey('answers.answer_id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))

	def __repr__(self):
		return '<downVote %r>' % (self.vote_id)
