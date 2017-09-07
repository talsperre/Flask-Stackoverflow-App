from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

"""This is the model for the answer class"""
class Answer(db.Model):
	__tablename__ = "answers"
	answer_id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	code = db.Column(db.Text)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
	comments = db.relationship('Comment', backref = 'answer', lazy = 'dynamic')
	upvotes = db.relationship('Upvote', backref = 'answer', lazy = 'dynamic')
	downvotes = db.relationship('Downvote', backref = 'answer', lazy = 'dynamic')

	def __repr__(self):
		return '<Answer %r>' % (self.body)