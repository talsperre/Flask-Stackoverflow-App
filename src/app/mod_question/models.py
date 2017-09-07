from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
#from app.mod_user.models import User

"""This is the model for question class"""
class Question(db.Model):
	__tablename__ = "questions"
	question_id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	body = db.Column(db.Text)
	code = db.Column(db.Text)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	answers = db.relationship('Answer', backref = 'question', lazy = 'dynamic')
	comments = db.relationship('Comment', backref = 'question', lazy = 'dynamic')
	tags = db.relationship('Tag', backref = 'question', lazy = 'dynamic')
	upvotes = db.relationship('Upvote', backref = 'question', lazy = 'dynamic')
	downvotes = db.relationship('Downvote', backref = 'question', lazy = 'dynamic')
	answered = db.Column(db.Integer) 

	def __repr__(self):
		return '<Question %r>' % (self.body)